from pyrogram import client, filters
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InputRichMessageContent,
    InputRichMessage,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQuery,
    CallbackQuery,
)
from TgShITBoT.strings import get_emoji
from TgShITBoT.Client import bot, app
import asyncio

E = lambda name: get_emoji(name, markdown=True)
I = lambda name: str(get_emoji(name))

def _is_owner(user_id: int) -> bool:
    return user_id == app.me.id

def _direction_buttons(target: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "Channel → Profile",
            callback_data=f"move:c2p:{target}",
            icon_custom_emoji_id=I("spark"),
        )],
        [InlineKeyboardButton(
            "Profile → Channel",
            callback_data=f"move:p2c:{target}",
            icon_custom_emoji_id=I("atsign"),
        )],
    ])


def _confirm_buttons(direction: str, target: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "Confirm",
            callback_data=f"move_exec:{direction}:{target}",
            icon_custom_emoji_id=I("CheckMark"),
        ),
        InlineKeyboardButton(
            "Cancel",
            callback_data="move_cancel",
            icon_custom_emoji_id=I("CrossMark"),
        ),
    ]])


def _summary_text(direction: str, target: str) -> str:
    if direction == "c2p":
        return (
            f"{E('TgAnimatedLogo')} **Move Username — Confirm**\n\n"
            f"{E('spark')} Direction: **Channel → Profile**\n"
            f"{E('atsign')} Username: `@{target}`\n\n"
            f"{E('settings')} **Steps:**\n"
            f"{E('wave')} Remove `@{target}` from the channel\n"
            f"{E('wave')} Set `@{target}` as your profile username"
        )
    return (
        f"{E('TgAnimatedLogo')} **Move Username — Confirm**\n\n"
        f"{E('atsign')} Direction: **Profile → Channel**\n"
        f"{E('spark')} Username: `@{target}`\n\n"
        f"{E('settings')} **Steps:**\n"
        f"{E('wave')} Remove `@{target}` from your profile\n"
        f"{E('wave')} Set `@{target}` as the channel username"
    )

@bot.on_inline_query(filters.regex(r"^move_usernames\s+@?(\w+)$"))
async def move_usernames(bot: client.Client, query: InlineQuery):
    if not _is_owner(query.from_user.id):
        return
    target = query.matches[0].group(1)

    await query.answer(
        results=[
            InlineQueryResultArticle(
                title="Move Username",
                description=f"Move @{target} between your profile and a channel",
                input_message_content=InputRichMessageContent(
                    rich_message=InputRichMessage(
                        markdown=(
                            f"{E('TgAnimatedLogo')} **Move Username**\n\n"
                            f"{E('atsign')} Target: `@{target}`\n\n"
                            f"{E('who')} Choose the direction:"
                        ),
                    ),
                ),
                reply_markup=_direction_buttons(target),
            ),
        ],
        cache_time=0,
    )


@bot.on_inline_query(filters.regex(r"^move_usernames\s*$"))
async def move_usernames_help(bot: client.Client, query: InlineQuery):
    if not _is_owner(query.from_user.id):
        return
    await query.answer(
        results=[
            InlineQueryResultArticle(
                title="Move Usernames — enter a username",
                description="Usage: move_usernames <username>",
                input_message_content=InputRichMessageContent(
                    rich_message=InputRichMessage(
                        markdown=(
                            f"{E('TgAnimatedLogo')} **Move Username**\n\n"
                            f"{E('who')} Usage: `@botname move_usernames <username>`\n\n"
                            f"{E('settings')} Replace `<username>` with the username you want to move."
                        ),
                    ),
                ),
            ),
        ],
        cache_time=0,
    )

@bot.on_callback_query(filters.regex(r"^move:(c2p|p2c):(\w+)$"))
async def move_direction_selected(bot: client.Client, cb: CallbackQuery):
    if not _is_owner(cb.from_user.id):
        return await cb.answer("⛔ Not allowed.", show_alert=True)
    direction = cb.matches[0].group(1)
    target = cb.matches[0].group(2)
    await cb.edit_message_text(
        text=_summary_text(direction, target),
        reply_markup=_confirm_buttons(direction, target),
    )
    await cb.answer()

@bot.on_callback_query(filters.regex(r"^move_exec:(c2p|p2c):(\w+)$"))
async def move_execute(bot: client.Client, cb: CallbackQuery):
    if not _is_owner(cb.from_user.id):
        return await cb.answer("⛔ Not allowed.", show_alert=True)
    direction = cb.matches[0].group(1)
    target = cb.matches[0].group(2)
    user: client.Client = app

    await cb.edit_message_text(
        f"{E('clock')} **Processing…** Please wait."
    )

    try:
        me = await user.get_me()
        if direction == "c2p":
            chat = await user.get_chat(target)
            await user.set_chat_username(chat_id=chat.id, username="")
            await asyncio.sleep(5)
            await user.set_username(username=target)
        else:
            chat = await user.create_channel(title=f"Hold {target}")
            await asyncio.sleep(2)
            await user.set_username(username="")
            await asyncio.sleep(5)
            await user.set_chat_username(chat_id=chat.id, username=target)
        await cb.edit_message_text(
            f"{E('CheckMark')} **Done!** Username moved successfully."
        )
    except Exception as e:
        await cb.edit_message_text(
            f"{E('CrossMark')} **Error:** `{e}`\n\n"
            f"{E('who')} Make sure you own both the username and the channel."
        )

    await cb.answer()

@bot.on_callback_query(filters.regex(r"^move_cancel$"))
async def move_cancel(bot: client.Client, cb: CallbackQuery):
    if not _is_owner(cb.from_user.id):
        return await cb.answer("⛔ Not allowed.", show_alert=True)
    await cb.edit_message_text(
        f"{E('CrossMark')} **Cancelled.** No changes were made."
    )
    await cb.answer()