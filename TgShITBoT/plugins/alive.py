from TgShITBoT.strings import cmds, get_emoji, PROJECT_NAME
from pyrogram.types import Message, LinkPreviewOptions
from TgShITBoT.config import PREFIXES, START_TIME
from pyrogram import filters, client
from TgShITBoT.Client import app
import platform, time, pyrogram, psutil, os

def get_uptime() -> str:
    seconds = int(time.time() - START_TIME)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    return " ".join(parts)


def get_ram_usage() -> str:
    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / (1024 * 1024)
    return f"{mem_mb:.1f} MB"


@app.on_message(
    filters.command(
        commands=cmds["alive"],
        prefixes=PREFIXES,
    )
    & filters.me
)
async def alive(user: client.Client, msg: Message):
    started_at = time.strftime("%Y-%m-%d %H:%M", time.localtime(START_TIME))
    text = (
        f"{get_emoji('TgAnimatedLogo', markdown=True)} **{PROJECT_NAME.lower()} is alive!**\n\n"
        f"{get_emoji('clock', markdown=True)} **Uptime:** `{get_uptime()}`\n"
        f"{get_emoji('snowflake', markdown=True)} **Started:** `{started_at}`\n"
        f"{get_emoji('leopard', markdown=True)} **Pyrogram:** `v{pyrogram.__version__}`\n"
        f"{get_emoji('spark', markdown=True)} **Python:** `{platform.python_version()}`\n"
        f"{get_emoji('settings', markdown=True)} **OS:** `{platform.system()} {platform.release()}`\n"
        f"{get_emoji('brain', markdown=True)} **CPU Usage:** `{psutil.cpu_percent()}%`\n"
        f"{get_emoji('github', markdown=True)} **Source:** [GitHub](https://github.com/muhmd101/TgShITBoT)\n"
        f"{get_emoji('zzz', markdown=True)} **RAM Usage:** `{get_ram_usage()}`\n\n"
        f"{get_emoji('who', markdown=True)} **Owner:** {msg.from_user.mention}"
    )
    await msg.edit_text(
        text=text,
        link_preview_options=LinkPreviewOptions(
            is_disabled=True
        )
    )
