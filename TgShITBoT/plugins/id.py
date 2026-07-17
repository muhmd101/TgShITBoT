from TgShITBoT.utils.registration import estimate_registration_date
from pyrogram.types import Message, LinkPreviewOptions
from TgShITBoT.strings import cmds, get_emoji
from TgShITBoT.config import PREFIXES
from pyrogram import filters, client
from TgShITBoT.Client import app

@app.on_message(
    filters.command(
        commands=cmds["id"],
        prefixes=PREFIXES
    )
    & filters.me
)
async def get_id(user: client.Client, msg: Message):
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
    if target.username:
        usernames.add(
            f"@{target.username}"
        )
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
    await msg.edit_text(
        text=caption,
        link_preview_options=LinkPreviewOptions(
            is_disabled=True
        )
    )
