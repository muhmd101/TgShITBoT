from TgShITBoT.strings import cmds, get_emoji
from TgShITBoT.config import PREFIXES
from pyrogram import filters, client
from TgShITBoT.Client import app, bot
from pyrogram.types import Message

E = lambda name: get_emoji(name, markdown=True)


@app.on_message(
    filters.command(
        commands=cmds["move"],
        prefixes=PREFIXES,
    )
    & filters.me
)
async def move_username(user: client.Client, msg: Message):
    if len(msg.command) < 2:
        return await msg.edit_text(
            f"{E('CrossMark')} **Usage:** `.move <username>`"
        )
    target = msg.command[1].lstrip("@")
    bot_me = await bot.get_me()
    result = await app.get_inline_bot_results(
        bot_me.username,
        query=f"move_usernames {target}",
    )
    await msg.delete()
    await app.send_inline_bot_result(
        msg.chat.id,
        result.query_id,
        result.results[0].id,
    )
