from TgShITBoT.strings import cmds, get_emoji
from TgShITBoT.config import PREFIXES
from pyrogram import filters, client, enums, types
from pyrogram.types import Message
from TgShITBoT.Client import app
import io, sys, traceback, textwrap, ast

@app.on_message(
    filters.command(
        commands=cmds["eval"],
        prefixes=PREFIXES
    )
    & filters.me
)
async def eval_code(user: client.Client, msg: Message):
    code = msg.text.split(maxsplit=1)
    if len(code) < 2:
        return await msg.edit_text(
            f"{get_emoji('scam', markdown=True)} **No code provided.**"
        )
    code = code[1]
    if code.startswith("```") and code.endswith("```"):
        code = code.strip("`")
        if code.startswith("python\n"):
            code = code[len("python\n"):]
    env = {
        **globals(),
        "app": user,
        "c": user,
        "client": user,
        "msg": msg,
        "message": msg,
        "reply": msg.reply_to_message,
        "chat": msg.chat,
        "enums": enums,
        "types": types,
    }
    tree = ast.parse(code)
    last_expr = None
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        last_expr = tree.body.pop()
    body_src = ast.unparse(tree) if tree.body else "pass"
    wrapped = "async def __eval():\n" + textwrap.indent(body_src, "    ")
    if last_expr:
        wrapped += "\n" + textwrap.indent(
            f"return {ast.unparse(last_expr.value)}", "    "
        )
    stdout = io.StringIO()
    try:
        exec(wrapped, env)
        func = env["__eval"]
        old_stdout = sys.stdout
        sys.stdout = stdout
        try:
            result = await func()
        finally:
            sys.stdout = old_stdout
        output = stdout.getvalue()
        if result is not None:
            output += repr(result)
    except Exception:
        output = traceback.format_exc()
    output = output.strip() or "None"
    if len(output) > 4000:
        output = output[:4000] + "\n... (truncated)"
    await msg.edit_text(
        f"{get_emoji('brain', markdown=True)} **Eval:**\n"
        f"```python\n{code}\n```\n"
        f"{get_emoji('spark', markdown=True)} **Output:**\n"
        f"```python\n{output}\n```"
    )