import json, os

def find_project_root():
	strings_dir = os.path.dirname(os.path.abspath(__file__))
	return os.path.dirname(strings_dir)

PROJECT_ROOT = find_project_root()
PROJECT_NAME = os.path.basename(PROJECT_ROOT)

EMOJIS_PATH = os.path.join(PROJECT_ROOT, "strings", "emojis.json")
CMDS_PATH = os.path.join(PROJECT_ROOT, "strings", "commands.json")

emojis = {}
cmds = {}

with open(EMOJIS_PATH, encoding="utf-8") as f:
	emojis = json.load(f)

with open(CMDS_PATH, encoding="utf-8") as f:
	cmds = json.load(f)

def get_emoji(
	name: str,
	markdown: bool = False,
) -> str | int:
	data = emojis[name]
	if markdown:
		return f"![{data['emoji']}](tg://emoji?id={data['id']})"
	return data["id"]