from TgShITBoT.strings import get_emoji, PROJECT_NAME
from pyrogram.types import Message, LinkPreviewOptions
from pyrogram import filters, client
from TgShITBoT.Client import bot


@bot.on_message(
    filters.command("start")
    & filters.private
)
async def start(bot: client.Client, msg: Message):
    await msg.reply_text(
        text=(
            f"{get_emoji('TgAnimatedLogo', markdown=True)} **Welcome to {PROJECT_NAME}!**\n\n"
            f"{get_emoji('spark', markdown=True)} I'm online and ready.\n"
            f"{get_emoji('settings', markdown=True)} Use /help to see available commands."
        ),
        link_preview_options=LinkPreviewOptions(
            is_disabled=True
        ),
    )
