from TgShITBoT.strings import cmds, get_emoji
from TgShITBoT.config import PREFIXES
from pyrogram import filters, client
from TgShITBoT.Client import app
from pyrogram.types import Message

@app.on_message(
    filters.command(
        commands=cmds["selfdestruct"],
        prefixes=PREFIXES,
    )
    & filters.me
)
async def toggle_self_destruction(user: client.Client, msg: Message):
    args = msg.command[1:]
    current = await user.db.get_self_destruction()
    if args and args[0].lower() == "set":
        args = args[1:]
    if args:
        arg = args[0].lower()
        if arg in ("on", "enable", "true"):
            new_state = True
        elif arg in ("off", "disable", "false"):
            new_state = False
        else:
            return await msg.edit_text(
                f"{get_emoji('CrossMark', markdown=True)} **Invalid argument.** "
                f"Use `{PREFIXES[0]}sd on` or `{PREFIXES[0]}sd off`."
            )
    else:
        new_state = not current
    await user.db.set_self_destruction(new_state)
    status = "enabled" if new_state else "disabled"
    emoji = "CheckMark" if new_state else "CrossMark"
    await msg.edit_text(
        f"{get_emoji(emoji, markdown=True)} **Self-destruct saver {status}.**"
    )