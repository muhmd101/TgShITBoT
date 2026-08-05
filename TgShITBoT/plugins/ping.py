from TgShITBoT.strings import cmds, get_emoji
from TgShITBoT.config import PREFIXES
from pyrogram import filters, client
from TgShITBoT.Client import app
from pyrogram.types import (
    Message,
)
import time


@app.on_message(
    filters.command(
        commands=cmds["ping"],
        prefixes=PREFIXES,
    )
    & filters.me
)
async def pinging(user: client.Client, msg: Message):
    start = time.perf_counter()
    sent = await msg.edit_text(
        f"{get_emoji('spark', markdown=True)} **Pinging...**"
    )
    end = time.perf_counter()
    latency = (end - start) * 1000
    await sent.edit_text(
        f"{get_emoji('spark', markdown=True)} **Pong!**\n"
        f"{get_emoji('clock', markdown=True)} `{latency:.2f} ms`"
    )