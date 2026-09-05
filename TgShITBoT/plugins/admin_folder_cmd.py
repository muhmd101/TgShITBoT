from TgShITBoT.strings import cmds, get_emoji
from TgShITBoT.utils.admin_folder import sync_admin_folder
from TgShITBoT.config import PREFIXES
from pyrogram import filters, client
from TgShITBoT.Client import app
from pyrogram.types import Message

E = lambda name: get_emoji(name, markdown=True)


@app.on_message(
    filters.command(
        commands=cmds["adminfolder"],
        prefixes=PREFIXES,
    )
    & filters.me
)
async def admin_folder_handler(user: client.Client, msg: Message):
    args = msg.command[1:]
    prefix = msg.text[0]

    if not args:
        return await msg.edit_text(
            f"{E('CrossMark')} **Usage:**\n"
            f"`{prefix}adminfolder sync` — force sync now\n"
            f"`{prefix}adminfolder list` — show admin chats\n"
            f"`{prefix}adminfolder status` — folder info"
        )

    sub = args[0].lower()

    if sub == "sync":
        await msg.edit_text(f"{E('settings')} **Syncing admin folder...**")
        await sync_admin_folder(user)
        count = len(await user.db.get_admin_chats())
        folder_id = await user.db.get_admin_folder_id()
        await msg.edit_text(
            f"{E('CheckMark')} **Admin folder synced.**\n"
            f"• Folder ID: `{folder_id}`\n"
            f"• Chats: `{count}`"
        )

    elif sub == "list":
        chat_ids = await user.db.get_admin_chats()
        if not chat_ids:
            return await msg.edit_text(
                f"{E('who')} **No admin chats tracked yet.**\n"
                f"Run `{prefix}adminfolder sync` first."
            )
        lines = [f"{E('leopard')} **Admin chats ({len(chat_ids)}):**"]
        for cid in sorted(chat_ids):
            try:
                chat = await user.get_chat(cid)
                title = chat.title or chat.first_name or str(cid)
                lines.append(f"• **{title}** (`{cid}`)")
            except Exception:
                lines.append(f"• `{cid}` (unresolved)")
        await msg.edit_text("\n".join(lines))

    elif sub == "status":
        folder_id = await user.db.get_admin_folder_id()
        chat_ids = await user.db.get_admin_chats()
        if folder_id is None:
            return await msg.edit_text(
                f"{E('who')} **No admin folder exists yet.**\n"
                f"Run `{prefix}adminfolder sync` to create one."
            )
        await msg.edit_text(
            f"{E('spark')} **Admin Folder Status**\n"
            f"• Folder ID: `{folder_id}`\n"
            f"• Tracked chats: `{len(chat_ids)}`"
        )

    else:
        await msg.edit_text(
            f"{E('CrossMark')} **Unknown sub-command.** "
            f"Use `sync`, `list`, or `status`."
        )
