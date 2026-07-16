from TgShITBoT.config import API_ID, API_HASH, SESSION_STRING
from TgShITBoT.strings import PROJECT_NAME
from TgShITBoT.database import DataBase
from pyrogram import Client

class Session(Client):
    def __init__(self):
        super().__init__(
            name="user",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION_STRING,
            plugins=dict(
                root=f"{PROJECT_NAME}.plugins",
            ),
        )
    async def start(self):
        await super().start()
        me = await self.get_me()
        self.db = DataBase(
            user_id=me.id
        )
        return me

app = Session()