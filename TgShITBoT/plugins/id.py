from TgShITBoT.utils.registration import estimate_registration_date
from pyrogram.types import Message, LinkPreviewOptions
from TgShITBoT.strings import cmds, get_emoji
from TgShITBoT.config import PREFIXES
from pyrogram import filters, client
from TgShITBoT.Client import app
import asyncio

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

    if target.is_self:
        chat_info = await user.get_chat(target.id)
        common = []
    else:
        chat_info, common = await asyncio.gather(
            user.get_chat(target.id),
            user.get_common_chats(target.id),
        )
    registration_str = estimate_registration_date(
        user_id=target.id
    ).strftime("%Y-%m")

    usernames = {f"@{target.username}"} if target.username else set()
    if target.usernames:
        usernames.update(f"@{u.username}" for u in target.usernames)

    badges = []
    if target.is_premium:
        badges.append(f"{get_emoji('star', markdown=True)} Premium")
    vs = target.verification_status
    if vs:
        if vs.is_verified:
            badges.append(f"{get_emoji('verified', markdown=True)} Verified")
        if vs.is_scam:
            badges.append(f"{get_emoji('scam', markdown=True)} Scam")
        if vs.is_fake:
            badges.append(f"{get_emoji('fake', markdown=True)} Fake")

    lines = [
        f"{get_emoji('id', markdown=True)} **ID:** `{target.id}`",
        f"{get_emoji('who', markdown=True)} **Name:** {target.mention}",
        f"{get_emoji('clock', markdown=True)} **Registered:** `{registration_str}`",
    ]
    if target.dc_id:
        lines.append(f"{get_emoji('settings', markdown=True)} **DC:** `{target.dc_id}`")
    if usernames:
        lines.append(f"{get_emoji('atsign', markdown=True)} **Username's**: {', '.join(usernames)}")
    if badges:
        lines.append(f"{get_emoji('sparkles', markdown=True)} **Badges:** {' | '.join(badges)}")
    if chat_info.bio:
        lines.append(f"{get_emoji('smile', markdown=True)} **Bio:** {chat_info.bio}")
    if common:
        lines.append(f"{get_emoji('leopard', markdown=True)} **Common groups:** `{len(common)}`")

    await msg.edit_text(
        text="\n".join(lines),
        link_preview_options=LinkPreviewOptions(
            is_disabled=True
        )
    )