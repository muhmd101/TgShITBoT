from TgShITBoT.utils.registration import estimate_registration_date
from TgShITBoT.strings import cmds, get_emoji
from pyrogram import filters, client, types
from TgShITBoT.config import PREFIXES
from pyrogram.types import Message
from TgShITBoT.Client import app


@app.on_message(
    filters.command(
        commands=cmds["id"],
        prefixes=PREFIXES
    )
    & filters.me
)
async def get_id(user: client.Client, msg: Message):
    chat_id = msg.chat.id
    if msg.reply_to_message:
        target = msg.reply_to_message.from_user
    elif len(msg.command) > 1:
        target = await user.get_users(msg.command[1])
    else:
        target = msg.from_user
    chat_info = await user.get_chat(target.id)
    registration_date = estimate_registration_date(
        user_id=target.id
    )
    registration_str = registration_date.strftime("%Y-%m")
    usernames = set()
    if target.usernames:
        for username in target.usernames:
            usernames.add(f"@{username.username}")
    usernames = list(usernames)
    badges = []
    if target.is_premium:
        badges.append(f"{get_emoji('star', markdown=True)} Premium")
    if target.verification_status:
        if target.verification_status.is_verified:
            badges.append(f"{get_emoji('verified', markdown=True)} Verified")
        if target.verification_status.is_scam:
            badges.append(f"{get_emoji('scam', markdown=True)} Scam")
        if target.verification_status.is_fake:
            badges.append(f"{get_emoji('fake', markdown=True)} Fake")
    caption = (
        f"{get_emoji('id', markdown=True)} **ID:** `{target.id}`\n"
        f"{get_emoji('who', markdown=True)} **Name:** {target.mention}\n"
        f"{get_emoji('clock', markdown=True)} **Registered:** `{registration_str}`"
    )
    if target.dc_id:
        caption += f"\n{get_emoji('settings', markdown=True)} **DC:** `{target.dc_id}`"
    if usernames:
        caption += f"\n{get_emoji('atsign', markdown=True)} **Username's**: {', '.join(usernames)}"
    if badges:
        caption += f"\n{get_emoji('sparkles', markdown=True)} **Badges:** {' | '.join(badges)}"
    if chat_info.bio:
        caption += f"\n{get_emoji('smile', markdown=True)} **Bio:** {chat_info.bio}"
    if target.id != user.me.id:
        common = await user.get_common_chats(target.id)
        if len(common):
            caption += f"\n{get_emoji('leopard', markdown=True)} **Common groups:** `{len(common)}`"
    photo_file_ids = []
    async for photo in user.get_chat_photos(target.id, limit=10):
        file_id = getattr(photo, "file_id", None)
        if file_id:
            photo_file_ids.append(file_id)
    if photo_file_ids:
        slides = "\n".join(f"![](tg://photo?id={fid})" for fid in photo_file_ids)
        caption += f"\n\n<tg-slideshow>\n\n{slides}\n\n</tg-slideshow>"
    await msg.delete()
    await user.send_rich_message(
        chat_id=chat_id,
        rich_message=types.InputRichMessage(markdown=caption),
    )
