from TgShITBoT.logger import LOGGER
from pyrogram import enums

log = LOGGER(__name__)

ADMIN_FOLDER_NAME = "Admin"


async def scan_admin_chats(client) -> set[int]:
    """Iterate all dialogs and return chat IDs where we are admin/creator."""
    admin_ids: set[int] = set()
    async for dialog in client.get_dialogs():
        chat = dialog.chat
        if chat.type not in (
            enums.ChatType.GROUP,
            enums.ChatType.SUPERGROUP,
            enums.ChatType.CHANNEL,
        ):
            continue
        if chat.is_admin or chat.is_creator:
            admin_ids.add(chat.id)
    return admin_ids


async def _find_existing_folder(client) -> int | None:
    """Find our managed admin folder by checking the stored ID, or by name."""
    folder_id = await client.db.get_admin_folder_id()
    if folder_id is not None:
        try:
            folders = await client.get_folders()
            for f in folders:
                if f.id == folder_id:
                    return folder_id
        except Exception:
            pass
        # Stored folder no longer exists
        await client.db.delete_admin_folder_id()
    # Try to find by name
    try:
        folders = await client.get_folders()
        for f in folders:
            if f.title == ADMIN_FOLDER_NAME:
                await client.db.set_admin_folder_id(f.id)
                return f.id
    except Exception:
        pass
    return None


async def sync_admin_folder(client) -> None:
    """Full sync: scan all dialogs, create/update the admin folder."""
    try:
        new_ids = await scan_admin_chats(client)
        old_ids = await client.db.get_admin_chats()
        folder_id = await _find_existing_folder(client)

        if folder_id is None:
            # Create the folder
            if not new_ids:
                log.info("No admin chats found, skipping folder creation.")
                return
            new_folder_id = await client.create_folder(
                name=ADMIN_FOLDER_NAME,
                included_chats=list(new_ids),
                excluded_chats=["me"],
            )
            await client.db.set_admin_folder_id(new_folder_id)
            await client.db.set_admin_chats(new_ids)
            log.info(
                f"Created '{ADMIN_FOLDER_NAME}' folder (id={new_folder_id}) "
                f"with {len(new_ids)} chats."
            )
        else:
            # Update existing folder if the set changed
            if new_ids != old_ids:
                await client.edit_folder(
                    folder_id=folder_id,
                    name=ADMIN_FOLDER_NAME,
                    included_chats=list(new_ids) if new_ids else [],
                    excluded_chats=["me"],
                )
                await client.db.set_admin_chats(new_ids)
                added = new_ids - old_ids
                removed = old_ids - new_ids
                log.info(
                    f"Updated '{ADMIN_FOLDER_NAME}' folder: "
                    f"+{len(added)} added, -{len(removed)} removed, "
                    f"{len(new_ids)} total."
                )
            else:
                log.info(
                    f"'{ADMIN_FOLDER_NAME}' folder is up to date "
                    f"({len(new_ids)} chats)."
                )
    except Exception as e:
        log.error(f"Admin folder sync failed: {e}")


async def check_chat_admin(client, chat) -> None:
    """
    Real-time check from an update handler.
    If admin and not tracked → add to folder.
    If not admin but tracked → remove from folder.
    """
    try:
        chat_id = chat.id
        chat_type = chat.type
        if chat_type not in (
            enums.ChatType.GROUP,
            enums.ChatType.SUPERGROUP,
            enums.ChatType.CHANNEL,
        ):
            return

        is_admin = chat.is_admin or chat.is_creator
        tracked = await client.db.get_admin_chats()
        already_tracked = chat_id in tracked

        if is_admin and not already_tracked:
            # New admin chat detected
            await client.db.add_admin_chat(chat_id)
            folder_id = await _find_existing_folder(client)
            if folder_id is not None:
                new_chats = tracked | {chat_id}
                await client.edit_folder(
                    folder_id=folder_id,
                    name=ADMIN_FOLDER_NAME,
                    included_chats=list(new_chats),
                    excluded_chats=["me"],
                )
                log.info(f"Added chat {chat_id} to admin folder.")
            else:
                # No folder yet — create one
                new_chats = tracked | {chat_id}
                new_folder_id = await client.create_folder(
                    name=ADMIN_FOLDER_NAME,
                    included_chats=list(new_chats),
                    excluded_chats=["me"],
                )
                await client.db.set_admin_folder_id(new_folder_id)
                log.info(
                    f"Created '{ADMIN_FOLDER_NAME}' folder with "
                    f"{len(new_chats)} chats (triggered by chat {chat_id})."
                )

        elif not is_admin and already_tracked:
            # Lost admin — remove from folder
            await client.db.remove_admin_chat(chat_id)
            folder_id = await _find_existing_folder(client)
            if folder_id is not None:
                new_chats = tracked - {chat_id}
                if new_chats:
                    await client.edit_folder(
                        folder_id=folder_id,
                        name=ADMIN_FOLDER_NAME,
                        included_chats=list(new_chats),
                        excluded_chats=["me"],
                    )
                else:
                    await client.delete_folder(folder_id)
                    await client.db.delete_admin_folder_id()
                log.info(f"Removed chat {chat_id} from admin folder.")
    except Exception:
        pass
