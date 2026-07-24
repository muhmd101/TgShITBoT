from pyrogram.types import Message, ReplyParameters
from TgShITBoT.strings import cmds, get_emoji
from TgShITBoT.config import PREFIXES
from pyrogram import filters, client
from pyrogram.errors import RPCError
from TgShITBoT.Client import app
import re

DURATION_RE = re.compile(r"^(\d+)([smhd])$", re.IGNORECASE)
UNIT_SECONDS = {"s": 1, "m": 60, "h": 3600, "d": 86400}

MIN_LIVE_PERIOD = 60
MAX_LIVE_PERIOD = 86400


def parse_duration(text: str) -> int | None:
    match = DURATION_RE.match(text.strip())
    if not match:
        return None
    value, unit = match.groups()
    return int(value) * UNIT_SECONDS[unit.lower()]


def parse_coords(text: str):
    parts = [p.strip() for p in text.split(",")]
    if len(parts) != 2:
        return None
    try:
        lat, lng = float(parts[0]), float(parts[1])
    except ValueError:
        return None
    if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
        return None
    return lat, lng


@app.on_message(
    filters.command(
        commands=cmds["livelocation"],
        prefixes=PREFIXES,
    )
    & filters.me
)
async def fake_live_location(user: client.Client, msg: Message):
    prefix = msg.text[0]
    raw = msg.text.split(maxsplit=1)
    if len(raw) < 2:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Usage:**\n"
            f"`{prefix}livelocation <lat>, <lng> <duration>`\n"
            f"**Example:** `{prefix}livelocation 25.826995, 42.196615 1h`\n"
            f"Duration units: `s` `m` `h` `d` (e.g. `30s`, `10m`, `2h`, `1d`)."
        )

    body = raw[1]
    tokens = body.rsplit(maxsplit=1)
    if len(tokens) != 2:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Missing duration.** "
            f"Example: `{prefix}livelocation 25.826995, 42.196615 1h`"
        )

    coords_part, duration_part = tokens

    coords = parse_coords(coords_part)
    if coords is None:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Invalid coordinates.** "
            f"Use `<lat>, <lng>`, e.g. `25.826995, 42.196615`."
        )

    seconds = parse_duration(duration_part)
    if seconds is None:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Invalid duration.** "
            f"Use a number + unit, e.g. `30s`, `10m`, `1h`, `2d`."
        )

    if seconds < MIN_LIVE_PERIOD:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Duration too short.** "
            f"Telegram requires live locations to run at least `{MIN_LIVE_PERIOD}s`."
        )
    if seconds > MAX_LIVE_PERIOD:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Duration too long.** "
            f"Max is `{MAX_LIVE_PERIOD}s` (`24h`)."
        )

    lat, lng = coords
    reply_params = None
    if msg.reply_to_message:
        reply_params = ReplyParameters(message_id=msg.reply_to_message.id)

    try:
        await user.send_location(
            chat_id=msg.chat.id,
            latitude=lat,
            longitude=lng,
            live_period=seconds,
            reply_parameters=reply_params,
        )
    except RPCError as e:
        return await msg.edit_text(
            f"{get_emoji('CrossMark', markdown=True)} **Failed to send location:** `{e}`"
        )

    try:
        await msg.delete()
    except RPCError:
        await msg.edit_text(
            f"{get_emoji('CheckMark', markdown=True)} **Live location sent.**"
        )
