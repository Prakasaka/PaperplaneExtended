# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module for executing code and terminal commands from Telegram. """

import asyncio
import time
import io
import traceback
from getpass import getuser
from os import remove
import sys
import subprocess
from telethon import events, sync, errors, functions, types
import inspect
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID
from telethon.errors import MessageEmptyError, MessageTooLongError, MessageNotModifiedError
from userbot.events import register
from userbot import MAX_MESSAGE_SIZE_LIMIT


@register(outgoing=True, pattern="^.eval(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    cmd = event.text.split(" ", maxsplit=1)[1]
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, event)
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
        evaluation = "Success"

    final_output = "**EVAL**: `{}` \n\n **OUTPUT**: \n`{}` \n".format(cmd, evaluation)

    if len(final_output) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id
            )
            await event.delete()
    else:
        await event.edit(final_output)


async def aexec(code, event):
    exec(
        f'async def __aexec(event): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__aexec'](event)


@register(outgoing=True, pattern=r"^.exec(?: |$)([\s\S]*)")
async def run(run_q):
    """ For .exec command, which executes the dynamically created program """
    if not run_q.text[0].isalpha() and run_q.text[0] not in ("/", "#", "@", "!"):
        if run_q.fwd_from:
            return
        DELAY_BETWEEN_EDITS = 0.3
        PROCESS_RUN_TIME = 100
        cmd = run_q.pattern_match.group(1)
        reply_to_id = run_q.message.id
        if run_q.reply_to_msg_id:
            reply_to_id = run_q.reply_to_msg_id
        start_time = time.time() + PROCESS_RUN_TIME
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**Output:**\n"
        stdout, stderr = await process.communicate()
        if len(stdout) > MAX_MESSAGE_SIZE_LIMIT:
            with io.BytesIO(str.encode(stdout)) as out_file:
                out_file.name = "exec.text"
                await run_q.client.send_file(
                    run_q.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption=OUTPUT,
                    reply_to=reply_to_id
                )
                await run_q.delete()
        if stderr.decode():
            await run_q.edit(f"{OUTPUT}`{stderr.decode()}`")
            return
        await run_q.edit(f"{OUTPUT}`{stdout.decode()}`")
   
        if BOTLOG:
            await run_q.client.send_message(
                BOTLOG_CHATID,
                "Exec query " + OUTPUT + " was executed successfully"
            )


@register(outgoing=True, pattern="^.term(?: |$)(.*)")
async def terminal_runner(term):
    """ For .term command, runs bash commands and scripts on your server. """
    if not term.text[0].isalpha() and term.text[0] not in ("/", "#", "@", "!"):
        curruser = getuser()
        command = term.pattern_match.group(1)
        try:
            from os import geteuid
            uid = geteuid()
        except ImportError:
            uid = "This ain't it chief!"

        if term.is_channel and not term.is_group:
            await term.edit("`Term commands aren't permitted on channels!`")
            return

        if not command:
            await term.edit("``` Give a command or use .help term for \
                an example.```")
            return

        if command in ("userbot.session", "config.env"):
            await term.edit("`That's a dangerous operation! Not Permitted!`")
            return

        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        result = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        if len(result) > 4096:
            output = open("output.txt", "w+")
            output.write(result)
            output.close()
            await term.client.send_file(
                term.chat_id,
                "output.txt",
                reply_to=term.id,
                caption="`Output too large, sending as file`",
            )
            remove("output.txt")
            return

        if uid is 0:
            await term.edit(
                "`"
                f"{curruser}:~# {command}"
                f"\n{result}"
                "`"
            )
        else:
            await term.edit(
                "`"
                f"{curruser}:~$ {command}"
                f"\n{result}"
                "`"
            )

        if BOTLOG:
            await term.client.send_message(
                BOTLOG_CHATID,
                "Terminal Command " + command + " was executed sucessfully",
            )

CMD_HELP.update({
    "eval": ".eval 2 + 3\nUsage: Evalute mini-expressions."
})
CMD_HELP.update({
    "exec": ".exec print('hello')\nUsage: Execute small python scripts."
})
CMD_HELP.update({
    "term": ".term ls\nUsage: Run bash commands and scripts on your server."
})
