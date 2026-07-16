# TgShITBoT

A userbot for Telegram built with [Kurigram](https://github.com/anomalyco/Kurigram) (Pyrogram fork).

## Features

| Plugin | Description |
|--------|-------------|
| Alive | Shows uptime, system stats, and version |
| Carbon | Renders code as a styled carbon image |
| Destruction | Saves self-destructing media automatically |
| Eval | Executes Python code inline |
| Help | Categorized command menu |
| ID | User info, registration date, DC, badges |
| Moderation | Mute, unmute, ban, unban, kick (persistent via Redis) |
| Ping | Response latency check |
| React | Auto-reactions on incoming PMs |

## Requirements

- Python 3.10+
- Redis server

## Installation

```bash
git clone https://github.com/muhmd101/TgShITBoT
cd TgShITBoT
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory:

```
API_ID=your_api_id
API_HASH=your_api_hash
SESSION_STRING=your_pyrogram_session
REDIS_DB_URI=redis://localhost:6379
```

Get `API_ID` and `API_HASH` from [my.telegram.org/apps](https://my.telegram.org/apps). Generate a session string using Pyrogram's [session generator](https://docs.pyrogram.org/api/methods/export_session_string).

## Usage

```bash
python -m TgShITBoT
```

## Commands

| Command | Aliases | Description |
|---------|---------|-------------|
| `.ping` | — | Bot latency |
| `.alive` | — | Uptime & info |
| `.id` | `whois` | User details |
| `.eval` | `exec`, `run` | Execute Python code |
| `.carbon` | `cb` | Code to carbon image |
| `.selfdestruct` | `sd` | Toggle auto-save self-destructing media |
| `.autoreact` | `ar` | Toggle auto-reactions |
| `.help` | `h` | Show help menu |
| `.mute` | — | Mute a user |
| `.unmute` | — | Unmute a user |
| `.ban` | — | Ban a user |
| `.unban` | — | Unban a user |
| `.kick` | — | Kick a user |
| `.mutedlist` | `muted` | List muted users |
| `.unmuteall` | — | Unmute all users |

Prefixes: `.`, `!`, `/`

## License

[MIT](LICENSE)
