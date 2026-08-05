from TgShITBoT.logger import LOGGER
from TgShITBoT.Client import app, bot
from TgShITBoT.config import BOT_TOKEN
import os, shutil, asyncio

class pycache:
	def __init__(self, root_dir):
		self.root_dir = root_dir
	def remove_folder(self, folder_path):
		if os.path.exists(folder_path):
			try:
				shutil.rmtree(folder_path)
			except:
				pass
	def delete(self):
		for dirpath, dirnames, filenames in os.walk(self.root_dir):
			for dirname in dirnames:
				if dirname == "__pycache__":
					pycache_dir = os.path.join(dirpath, dirname)
					self.remove_folder(pycache_dir)


async def ensure_bot_inline(bot_me):
	if bot_me.inline_query_placeholder:
		return
	LOGGER(__name__).info("Inline mode not enabled, setting up via BotFather...")
	await app.send_message("BotFather", "/setinline")
	await asyncio.sleep(1)
	await app.send_message("BotFather", f"@{bot_me.username}")
	await asyncio.sleep(1)
	await app.send_message("BotFather", "inline")
	await asyncio.sleep(1)
	LOGGER(__name__).info("Inline mode enabled successfully")

async def run():
	me = await app.start()
	pycache("./").delete()
	LOGGER(__name__).info(
		f"[{me.full_name}] started successfully"
	)
	if BOT_TOKEN:
		bot_me = await bot.start()
		LOGGER(__name__).info(
			f"[{bot_me.first_name}] (bot) started successfully"
		)
		await ensure_bot_inline(bot_me)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(run())
loop.run_forever()
