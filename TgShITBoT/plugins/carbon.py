from TgShITBoT.strings import cmds, get_emoji
from TgShITBoT.config import PREFIXES
from pyrogram import filters, client
from pyrogram.errors import RPCError
from TgShITBoT.Client import app
from pyrogram.types import Message
import aiohttp
import io


@app.on_message(
    filters.command(
        commands=cmds["carbon"],
        prefixes=PREFIXES,
    )
    & filters.me
)
async def carbon(user: client.Client, msg: Message):
    if msg.reply_to_message and msg.reply_to_message.text:
        code = msg.reply_to_message.text
    elif len(msg.command) > 1:
        code = msg.text.split(maxsplit=1)[1]
    else:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Reply to code or provide code to render.**"
        )

    if code.startswith("```") and code.endswith("```"):
        code = code.strip("`")
        if code.startswith("python\n"):
            code = code[len("python\n"):]

    await msg.edit_text(
        f"{get_emoji('spark', markdown=True)} **Rendering...**"
    )

    payload = {
        "code": code,
        "language": "python",
        "theme": "one-hunter",
        "mode": "dark",
        "background": "midnight",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://ray.tinte.dev/api/v1/screenshot",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=20),
            ) as resp:
                if resp.status != 200:
                    return await msg.edit_text(
                        f"{get_emoji('CrossMark', markdown=True)} **Ray API error:** `{resp.status}`"
                    )
                image_bytes = await resp.read()
    except aiohttp.ClientError as e:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Request failed:** `{e}`"
        )
    except Exception as e:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Unexpected error:** `{e}`"
        )
    photo = io.BytesIO(image_bytes)
    photo.name = "carbon.png"
    try:
        await msg.reply_photo(photo=photo)
        await msg.delete()
    except RPCError as e:
        await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Telegram error:** `{e}`"
        )