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

    async def set_auto_sticker(self, enabled: bool) -> None:
        await self.redis.set(
            self._k("auto_sticker"),
            "1" if enabled else "0",
        )

    async def get_auto_sticker(self) -> bool:
        value = await self.redis.get(self._k("auto_sticker"))
        return value == "1"

    async def add_sticker_pack(self, name: str, file_ids: list[str]) -> None:
        await self.redis.sadd(self._k("sticker_packs"), name)
        if file_ids:
            await self.redis.sadd(self._k(f"sticker_pack:{name}"), *file_ids)

    async def remove_sticker_pack(self, name: str) -> None:
        await self.redis.srem(self._k("sticker_packs"), name)
        await self.redis.delete(self._k(f"sticker_pack:{name}"))

    async def get_sticker_packs(self) -> dict[str, list[str]]:
        names = await self.redis.smembers(self._k("sticker_packs"))
        packs = {}
        for name in names:
            file_ids = await self.redis.smembers(self._k(f"sticker_pack:{name}"))
            packs[name] = list(file_ids)
        return packs

    async def add_muted_global(self, user_id: int) -> None:
        await self.redis.sadd(self._k("muted_global"), user_id)

    async def remove_muted_global(self, user_id: int) -> None:
        await self.redis.srem(self._k("muted_global"), user_id)

    async def get_muted_global(self) -> list[int]:
        members = await self.redis.smembers(self._k("muted_global"))
        return [int(m) for m in members]

    async def clear_muted_global(self) -> None:
        await self.redis.delete(self._k("muted_global"))

    async def is_muted_global(self, user_id: int) -> bool:
        return await self.redis.sismember(self._k("muted_global"), user_id)
