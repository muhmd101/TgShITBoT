from TgShITBoT.strings import cmds, get_emoji
from TgShITBoT.config import PREFIXES
from pyrogram import filters, client
from pyrogram.errors import (
    ChatAdminRequired,
    UserAdminInvalid,
    UserNotParticipant,
    PeerIdInvalid,
    UsernameNotOccupied,
    UsernameInvalid,
    FloodWait,
    RPCError,
)
from TgShITBoT.Client import app
from pyrogram.types import Message


@app.on_message(
    filters.command(
        commands=cmds["mute"],
        prefixes=PREFIXES,
    )
    & filters.me
)
async def mute_user(user: client.Client, msg: Message):
    if msg.reply_to_message:
        target = msg.reply_to_message.from_user
    elif len(msg.command) > 1:
        arg = msg.command[1]
        try:
            target = await user.get_users(int(arg) if arg.isdigit() else arg)
        except (PeerIdInvalid, UsernameNotOccupied, UsernameInvalid):
            return await msg.edit_text(
                f"{get_emoji('CrossMark', markdown=True)} **Couldn't find that user.**"
            )
    else:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Reply to a user or provide an ID/username.**"
        )

    await user.db.add_muted_global(target.id)
    await msg.edit_text(
        f"{get_emoji('CheckMark', markdown=True)} **Muted** {target.mention} **globally.**"
    )


@app.on_message(
    filters.command(
        commands=cmds["unmute"],
        prefixes=PREFIXES,
    )
    & filters.me
)
async def unmute_user(user: client.Client, msg: Message):
    if msg.reply_to_message:
        target = msg.reply_to_message.from_user
    elif len(msg.command) > 1:
        arg = msg.command[1]
        try:
            target = await user.get_users(int(arg) if arg.isdigit() else arg)
        except (PeerIdInvalid, UsernameNotOccupied, UsernameInvalid):
            return await msg.edit_text(
                f"{get_emoji('CrossMark', markdown=True)} **Couldn't find that user.**"
            )
    else:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Reply to a user or provide an ID/username.**"
        )

    await user.db.remove_muted_global(target.id)
    await msg.edit_text(
        f"{get_emoji('CheckMark', markdown=True)} **Unmuted** {target.mention} **globally.**"
    )


@app.on_message(
    filters.command(
        commands=cmds["ban"],
        prefixes=PREFIXES,
    )
    & filters.me
    & filters.group
)
async def ban_user(user: client.Client, msg: Message):
    if msg.reply_to_message:
        target = msg.reply_to_message.from_user
    elif len(msg.command) > 1:
        arg = msg.command[1]
        try:
            target = await user.get_users(int(arg) if arg.isdigit() else arg)
        except (PeerIdInvalid, UsernameNotOccupied, UsernameInvalid):
            return await msg.edit_text(
                f"{get_emoji('CrossMark', markdown=True)} **Couldn't find that user.**"
            )
    else:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Reply to a user or provide an ID/username.**"
        )
    try:
        await user.ban_chat_member(
            chat_id=msg.chat.id,
            user_id=target.id,
        )
    except ChatAdminRequired:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **I'm not an admin in this chat.**"
        )
    except UserAdminInvalid:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Can't ban this user (they may be an admin, or I lack permission).**"
        )
    except UserNotParticipant:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **That user isn't in this chat.**"
        )
    except FloodWait as e:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Flood wait — try again in {e.value}s.**"
        )
    except RPCError as e:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Telegram error:** `{e}`"
        )
    await msg.edit_text(
        f"{get_emoji('CheckMark', markdown=True)} **Banned** {target.mention}"
    )


@app.on_message(
    filters.command(
        commands=cmds["unban"],
        prefixes=PREFIXES,
    )
    & filters.me
    & filters.group
)
async def unban_user(user: client.Client, msg: Message):
    if msg.reply_to_message:
        target = msg.reply_to_message.from_user
    elif len(msg.command) > 1:
        arg = msg.command[1]
        try:
            target = await user.get_users(int(arg) if arg.isdigit() else arg)
        except (PeerIdInvalid, UsernameNotOccupied, UsernameInvalid):
            return await msg.edit_text(
                f"{get_emoji('CrossMark', markdown=True)} **Couldn't find that user.**"
            )
    else:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Reply to a user or provide an ID/username.**"
        )
    try:
        await user.unban_chat_member(
            chat_id=msg.chat.id,
            user_id=target.id,
        )
    except ChatAdminRequired:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **I'm not an admin in this chat.**"
        )
    except FloodWait as e:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Flood wait — try again in {e.value}s.**"
        )
    except RPCError as e:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Telegram error:** `{e}`"
        )
    await msg.edit_text(
        f"{get_emoji('CheckMark', markdown=True)} **Unbanned** {target.mention}"
    )


@app.on_message(
    filters.command(
        commands=cmds["kick"],
        prefixes=PREFIXES,
    )
    & filters.me
    & filters.group
)
async def kick_user(user: client.Client, msg: Message):
    if msg.reply_to_message:
        target = msg.reply_to_message.from_user
    elif len(msg.command) > 1:
        arg = msg.command[1]
        try:
            target = await user.get_users(int(arg) if arg.isdigit() else arg)
        except (PeerIdInvalid, UsernameNotOccupied, UsernameInvalid):
            return await msg.edit_text(
                f"{get_emoji('CrossMark', markdown=True)} **Couldn't find that user.**"
            )
    else:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Reply to a user or provide an ID/username.**"
        )
    try:
        await user.ban_chat_member(
            chat_id=msg.chat.id,
            user_id=target.id,
        )
        await user.unban_chat_member(
            chat_id=msg.chat.id,
            user_id=target.id,
        )
    except ChatAdminRequired:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **I'm not an admin in this chat.**"
        )
    except UserAdminInvalid:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Can't kick this user (they may be an admin, or I lack permission).**"
        )
    except UserNotParticipant:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **That user isn't in this chat.**"
        )
    except FloodWait as e:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Flood wait — try again in {e.value}s.**"
        )
    except RPCError as e:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Telegram error:** `{e}`"
        )
    await msg.edit_text(
        f"{get_emoji('CheckMark', markdown=True)} **Kicked** {target.mention}"
    )

@app.on_message(
    filters.command(
        commands=cmds["unmuteall"],
        prefixes=PREFIXES,
    )
    & filters.me
)
async def unmute_all(user: client.Client, msg: Message):
    try:
        muted_ids = await user.db.get_muted_global()
    except Exception as e:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Database error:** `{e}`"
        )
    if not muted_ids:
        return await msg.edit_text(
            f"{get_emoji('who', markdown=True)} **No globally muted users.**"
        )
    try:
        await user.db.clear_muted_global()
    except Exception as e:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Failed to clear database:** `{e}`"
        )
    await msg.edit_text(
        f"{get_emoji('CheckMark', markdown=True)} **Unmuted all** `{len(muted_ids)}` **user(s) globally.**"
    )

@app.on_message(
    filters.command(
        commands=cmds["mutedlist"],
        prefixes=PREFIXES,
    )
    & filters.me
)
async def muted_list(user: client.Client, msg: Message):
    try:
        muted_ids = await user.db.get_muted_global()
    except Exception as e:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Database error:** `{e}`"
        )
    if not muted_ids:
        return await msg.edit_text(
            f"{get_emoji('who', markdown=True)} **No globally muted users.**"
        )
    lines = []
    for uid in muted_ids:
        try:
            member = await user.get_users(uid)
            lines.append(f"• {member.mention} (`{uid}`)")
        except RPCError:
            lines.append(f"• `{uid}` (unresolved)")
    text = (
        f"{get_emoji('who', markdown=True)} **Globally muted users ({len(muted_ids)}):**\n"
        + "\n".join(lines)
    )
    await msg.edit_text(text)