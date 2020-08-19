#credits to @mrconfused 
import io
import sys
import asyncio
import inspect
import traceback
from .. import CMD_HELP
from telethon import events, errors, functions, types
from ..utils import admin_cmd, sudo_cmd, edit_or_reply

@borg.on(admin_cmd(pattern="calc (.*)"))
async def _(event):
    cmd = event.text.split(" ", maxsplit=1)[1]
    event = await edit_or_reply(event ,"Calculating ...")
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(san, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Sorry I cant find result for the given equation"
    final_output = "**EQUATION**: `{}` \n\n **SOLUTION**: \n`{}` \n".format(cmd, evaluation)
    await event.edit(final_output)

async def aexec(code, event):
    exec(
        f'async def __aexec(event): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__aexec'](event)

CMD_HELP.update({"calc": 
      "**SYNTAX : **`.calc` your equation :\
      \n**USAGE : **solves the given maths equation by bodmass rule. "
}) 
