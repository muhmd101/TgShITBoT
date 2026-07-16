from TgShITBoT.logger import LOGGER
from TgShITBoT.Client import app
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

async def run():
	me = await app.start()
	pycache("./").delete()
	LOGGER(__name__).info(
		f"[{me.full_name}] started successfully"
	)

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(run())
loop.run_forever()