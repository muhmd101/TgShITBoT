from TgShITBoT.strings import cmds, get_emoji, PROJECT_NAME
from pyrogram.types import Message, LinkPreviewOptions
from TgShITBoT.config import PREFIXES
from pyrogram import filters, client
from TgShITBoT.Client import app

CATEGORIES = {
    "General": {
        "emoji": "spark",
        "commands": {
            "ping": "check ping",
            "alive": "check if bot is alive",
            "id": "get user/chat info (reply/username/ID)",
            "eval": "evaluate Python code",
        },
    },
    "Moderation": {
        "emoji": "leopard",
        "commands": {
            "mute": "mute a user (reply/username/ID) [duration]",
            "unmute": "unmute a user (reply/username/ID)",
            "ban": "ban a user (reply/username/ID)",
            "unban": "unban a user (reply/username/ID)",
            "kick": "kick a user (reply/username/ID)",
            "muted": "list muted users in this chat",
            "unmuteall": "unmute everyone in this chat",
        },
    },
    "Utility": {
        "emoji": "settings",
        "commands": {
            "selfdestruct": "toggle saving self-destruct media",
            "location": "send a fake live location - `<lat>, <lng> <duration>` (e.g. `1h`, `15s`)",
        },
    },
    "Auto": {
        "emoji": "settings",
        "commands": {
            "auto react set on/off": "toggle auto-react on private messages",
            "auto sticker set on/off": "toggle auto-sticker on private messages",
            "auto sticker pack": "reply to a sticker to add its pack",
            "auto sticker packs": "list added sticker packs",
            "auto sticker pack remove": "reply to a sticker to remove its pack",
        },
    },
}


@app.on_message(
    filters.command(
        commands=cmds["help"],
        prefixes=PREFIXES,
    )
    & filters.me
)
async def help_menu(user: client.Client, msg: Message):
    prefix = msg.text[0]
    prefixes_str = " ".join(f"`{p}`" for p in PREFIXES)
    lines = [
        f"{get_emoji('TgAnimatedLogo', markdown=True)} **{PROJECT_NAME} — Commands**",
        f"{get_emoji('settings', markdown=True)} **Prefixes:** {prefixes_str}\n",
    ]
    for category, data in CATEGORIES.items():
        lines.append(f"{get_emoji(data['emoji'], markdown=True)} **{category}**")
        for name, description in data["commands"].items():
            aliases = cmds.get(name, name)
            aliases = [aliases] if isinstance(aliases, str) else list(aliases)
            formatted = " / ".join(f"`{prefix}{a}`" for a in aliases)
            lines.append(f"• {formatted} - {description}")
        lines.append("")

    lines.append(f"{get_emoji('who', markdown=True)} **Help**")
    help_aliases = cmds["help"]
    help_aliases = [help_aliases] if isinstance(help_aliases, str) else list(help_aliases)
    lines.append(
        "• " + " / ".join(f"`{prefix}{a}`" for a in help_aliases)
        + " - show this help message"
    )
    text = "\n".join(lines)
    await msg.edit_text(
        text=text,
        link_preview_options=LinkPreviewOptions(
            is_disabled=True
        )
    )
