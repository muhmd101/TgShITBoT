from TgShITBoT.config import REDIS_DB_URI
import redis.asyncio as db

class DataBase:
    def __init__(self, user_id: int):
        self.redis = db.from_url(
            url=REDIS_DB_URI,
            decode_responses=True,
        )
        self.user_id = user_id

    def _k(self, suffix: str) -> str:
        return f"{self.user_id}:{suffix}"

    async def set_self_destruction(self, enabled: bool) -> None:
        await self.redis.set(
            self._k("self_destruction"),
            "1" if enabled else "0",
        )

    async def get_self_destruction(self) -> bool:
        value = await self.redis.get(self._k("self_destruction"))
        return value == "1"

    async def add_muted(self, chat_id: int, user_id: int) -> None:
        await self.redis.sadd(self._k(f"muted:{chat_id}"), user_id)

    async def remove_muted(self, chat_id: int, user_id: int) -> None:
        await self.redis.srem(self._k(f"muted:{chat_id}"), user_id)

    async def get_muted(self, chat_id: int) -> list[int]:
        members = await self.redis.smembers(self._k(f"muted:{chat_id}"))
        return [int(m) for m in members]
    async def clear_muted(self, chat_id: int) -> None:
        await self.redis.delete(self._k(f"muted:{chat_id}"))
    async def set_auto_react(self, enabled: bool) -> None:
        await self.redis.set(
            self._k("auto_react"),
            "1" if enabled else "0",
        )
    async def get_auto_react(self) -> bool:
        value = await self.redis.get(self._k("auto_react"))
        return value == "1"