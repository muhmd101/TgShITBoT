from TgShITBoT.strings import cmds, get_emoji
from TgShITBoT.config import PREFIXES
from pyrogram import filters, client
from pyrogram.errors import RPCError
from TgShITBoT.Client import app
from pyrogram.types import Message
import random

REACTION_EMOJIS = [get_emoji("smile"), get_emoji("wave"), get_emoji("snowflake")]


@app.on_message(
    filters.command(
        commands=cmds["autoreact"],
        prefixes=PREFIXES,
    )
    & filters.me
)
async def toggle_auto_react(user: client.Client, msg: Message):
    args = msg.command[1:]
    current = await user.db.get_auto_react()

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
                f"Use `{PREFIXES[0]}autoreact on` or `{PREFIXES[0]}autoreact off`."
            )
    else:
        new_state = not current

    await user.db.set_auto_react(new_state)
    status = "enabled" if new_state else "disabled"
    emoji = "CheckMark" if new_state else "CrossMark"
    await msg.edit_text(
        f"{get_emoji(emoji, markdown=True)} **Auto-react {status}.**"
    )


@app.on_message(
    filters.private
    & ~filters.me
)
async def auto_react_handler(user: client.Client, msg: Message):
    if not await user.db.get_auto_react():
        return
    if random.random() > 0.4:
        return
    emoji = random.choice(REACTION_EMOJIS)
    try:
        await user.send_reaction(
            chat_id=msg.chat.id,
            message_id=msg.id,
            emoji=emoji,
        )
    except RPCError:
        pass
