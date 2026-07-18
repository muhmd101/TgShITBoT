from TgShITBoT.strings import cmds, get_emoji
from TgShITBoT.config import PREFIXES
from pyrogram import filters, client
from pyrogram.errors import RPCError
from TgShITBoT.Client import app
from pyrogram.types import Message

def parse_on_off(args):
    """Returns True / False / 'toggle' (no args) / None (invalid)."""
    if args and args[0].lower() == "set":
        args = args[1:]
    if not args:
        return "toggle"
    arg = args[0].lower()
    if arg in ("on", "enable", "true"):
        return True
    if arg in ("off", "disable", "false"):
        return False
    return None


@app.on_message(
    filters.command(
        commands=cmds["auto"],
        prefixes=PREFIXES,
    )
    & filters.me
)
async def auto_handler(user: client.Client, msg: Message):
    prefix = msg.text[0]
    args = msg.command[1:]
    if not args:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Usage:**\n"
            f"`{prefix}auto react set on/off`\n"
            f"`{prefix}auto sticker set on/off`\n"
            f"`{prefix}auto sticker pack` (reply to a sticker)\n"
            f"`{prefix}auto sticker packs` (list added packs)"
        )

    sub = args[0].lower()
    rest = args[1:]

    if sub == "react":
        await _handle_react(user, msg, rest, prefix)
    elif sub == "sticker":
        await _handle_sticker(user, msg, rest, prefix)
    else:
        await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Unknown sub-command.** "
            f"Use `react` or `sticker`."
        )


async def _handle_react(user: client.Client, msg: Message, args, prefix: str):
    current = await user.db.get_auto_react()
    result = parse_on_off(args)
    if result is None:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Invalid argument.** "
            f"Use `{prefix}auto react set on` or `{prefix}auto react set off`."
        )
    new_state = (not current) if result == "toggle" else result
    await user.db.set_auto_react(new_state)
    status = "enabled" if new_state else "disabled"
    emoji = "CheckMark" if new_state else "CrossMark"
    await msg.edit_text(
        f"{get_emoji(emoji, markdown=True)} **Auto React {status}.**"
    )


async def _handle_sticker(user: client.Client, msg: Message, args, prefix: str):
    if args and args[0].lower() == "pack":
        pack_args = args[1:]
        if pack_args and pack_args[0].lower() == "remove":
            return await _remove_sticker_pack(user, msg)
        return await _add_sticker_pack(user, msg)

    if args and args[0].lower() == "packs":
        return await _list_sticker_packs(user, msg, prefix)

    current = await user.db.get_auto_sticker()
    result = parse_on_off(args)
    if result is None:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Invalid argument.** "
            f"Use `{prefix}auto sticker set on`, `{prefix}auto sticker set off`, "
            f"or reply to a sticker with `{prefix}auto sticker pack`."
        )
    new_state = (not current) if result == "toggle" else result
    await user.db.set_auto_sticker(new_state)
    status = "enabled" if new_state else "disabled"
    emoji = "CheckMark" if new_state else "CrossMark"
    await msg.edit_text(
        f"{get_emoji(emoji, markdown=True)} **Auto Sticker {status}.**"
    )


async def _add_sticker_pack(user: client.Client, msg: Message):
    reply = msg.reply_to_message
    if not reply or not reply.sticker:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Reply to a sticker to add its pack.**"
        )
    set_name = reply.sticker.set_name
    if not set_name:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **That sticker doesn't belong to a pack.**"
        )
    packs = await user.db.get_sticker_packs()
    if set_name in packs:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Pack** `{set_name}` **is already added.**"
        )
    try:
        stickers = await user.get_stickers(set_name)
    except RPCError as e:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Couldn't fetch pack:** `{e}`"
        )
    file_ids = [s.file_id for s in stickers]
    if not file_ids:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **That pack has no stickers.**"
        )
    await user.db.add_sticker_pack(set_name, file_ids)
    await msg.edit_text(
        f"{get_emoji('CheckMark', markdown=True)} **Added pack** `{set_name}` "
        f"**(`{len(file_ids)}` stickers).**"
    )


async def _remove_sticker_pack(user: client.Client, msg: Message):
    reply = msg.reply_to_message
    set_name = None
    if reply and reply.sticker:
        set_name = reply.sticker.set_name
    if not set_name:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Reply to a sticker from the pack you want to remove.**"
        )
    packs = await user.db.get_sticker_packs()
    if set_name not in packs:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Pack** `{set_name}` **isn't added.**"
        )
    await user.db.remove_sticker_pack(set_name)
    await msg.edit_text(
        f"{get_emoji('CheckMark', markdown=True)} **Removed pack** `{set_name}`."
    )


async def _list_sticker_packs(user: client.Client, msg: Message, prefix: str):
    packs = await user.db.get_sticker_packs()
    if not packs:
        return await msg.edit_text(
            f"{get_emoji('who', markdown=True)} **No sticker packs added yet.**\n"
            f"Reply to a sticker with `{prefix}auto sticker pack` to add one."
        )
    lines = [f"{get_emoji('sparkles', markdown=True)} **Sticker packs ({len(packs)}):**"]
    for name, stickers in packs.items():
        lines.append(f"• `{name}` — `{len(stickers)}` stickers")
    await msg.edit_text("\n".join(lines))