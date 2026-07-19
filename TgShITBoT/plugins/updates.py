from TgShITBoT.strings import get_emoji, emojis
from pyrogram.raw import functions, types
from pyrogram import filters, client
from pyrogram.types import Message
from pyrogram.file_id import FileId
from TgShITBoT.Client import app
import random, os

REACTION_EMOJIS = [get_emoji(name) for name in emojis]


@app.on_message(
    filters.private
    & ~ filters.me
    & ~ filters.bot
    & ~ filters.service
)
async def private_update_handler(user: client.Client, msg: Message):
    if not msg.from_user:
        return
    try:
        is_muted = await user.db.is_muted_global(msg.from_user.id)
    except Exception:
        is_muted = False
    if is_muted:
        try:
            await msg.delete()
        except:
            pass
        return
    if await filters.self_destruction(user, msg):
        if await user.db.get_self_destruction():
            file = await msg.download()
            await user.send_document(
                chat_id="me",
                document=file
            )
            os.remove(file)
    if await user.db.get_auto_react() and random.random() <= 0.2:
        emoji = random.choice(REACTION_EMOJIS)
        try:
            await msg.react(emoji=emoji)
        except:
            pass
    if await user.db.get_auto_sticker():
        packs = await user.db.get_sticker_packs()
        all_stickers = [fid for stickers in packs.values() for fid in stickers]
        if all_stickers and random.random() <= 0.2:
            sticker = random.choice(all_stickers)
            try:
                await user.send_sticker(
                    chat_id=msg.chat.id,
                    sticker=sticker,
                )
                decoded = FileId.decode(sticker)
                await user.invoke(
                    functions.messages.SaveRecentSticker(
                        id=types.InputDocument(
                            id=decoded.media_id,
                            access_hash=decoded.access_hash,
                            file_reference=decoded.file_reference,
                        ),
                        unsave=True
                    )
                )
            except:
                pass


@app.on_message(
    filters.group
    & filters.admin
    & ~ filters.me
    & ~ filters.bot
    & ~ filters.service
    & ~ filters.linked_channel
)
async def group_update_handler(user: client.Client, msg: Message):
    if not msg.from_user:
        return
    try:
        is_muted = await user.db.is_muted_global(msg.from_user.id)
    except Exception:
        return
    if not is_muted:
        return
    try:
        await msg.delete()
    except:
        pass
