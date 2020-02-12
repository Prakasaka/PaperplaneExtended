# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD

""" Userbot module for other small commands. """

from random import randint
from time import sleep
import os
import sys
from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register



# Copyright (c) Gegham Zakaryan | 2019
#
@register(outgoing=True, pattern="^.repeat (.*) (.*)")
async def repeat(rep):
    if not rep.text[0].isalpha() and rep.text[0] not in ("/", "#", "@", "!"):
        replyCount = int(rep.pattern_match.group(1))
        toBeRepeated = rep.pattern_match.group(2)

        replyText = toBeRepeated + "\n"

        for i in range(0, replyCount-1):
            replyText += toBeRepeated + "\n"

        await rep.edit(replyText)

@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    """ For .repo command, just returns the repo URL. """
    if not wannasee.text[0].isalpha() and wannasee.text[0] not in ("/", "#", "@", "!"):
        await wannasee.edit("Click [here](https://github.com/AvinashReddy3108/PaperplaneExtended) to open Paperplane Extended's GitHub page.")
