from TgShITBoT.config import API_ID, API_HASH, SESSION_STRING, BOT_TOKEN
from TgShITBoT.strings import PROJECT_NAME
from TgShITBoT.database import DataBase
from pyrogram import Client, enums
from pathlib import Path

def get_bot_plugin_excludes(root: str, sub_pkg: str) -> list[str]:
    root_dir = Path(root.replace(".", "/"))
    bot_dir = root_dir / sub_pkg.replace(".", "/")
    excludes = []
    for path in sorted(bot_dir.rglob("*.py")):
        if path.stem == "__init__":
            continue
        rel_path = path.relative_to(root_dir).with_suffix("")
        module_path = ".".join(rel_path.parts)
        excludes.append(module_path)
    return excludes


class UserSession(Client):
    def __init__(self):
        super().__init__(
            name="user",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION_STRING,
            plugins=dict(
                root=f"{PROJECT_NAME}.plugins",
                exclude=get_bot_plugin_excludes(f"{PROJECT_NAME}.plugins", "bot"),
            ),
        )
    async def start(self):
        await super().start()
        me = await self.get_me()
        self.db = DataBase(user_id=me.id)
        return me


class BotSession(Client):
    def __init__(self):
        super().__init__(
            name="bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            in_memory=True,
            parse_mode=enums.ParseMode.MARKDOWN,
            plugins=dict(
                root=f"{PROJECT_NAME}.plugins.bot",
            ),
        )
    async def start(self):
        await super().start()
        me = await self.get_me()
        return me


app = UserSession()
bot = BotSession()
