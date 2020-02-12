# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
#

""" Userbot module for having some fun with people. """

import asyncio
import random
import re

from userbot.events import register

@register(outgoing=True, pattern="^.oof$")
async def Oof(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        t = "Oof"
        for j in range(15):
            t = t[:-1] + "of"
            await e.edit(t)


@register(outgoing=True, pattern=r"\.f (.*)")
async def payf(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        p = e.pattern_match.group(1)
        pay = f"{p*8}\n{p*8}\n{p*2}\n{p*2}\n{p*2}\n{p*6}\n{p*6}\n{p*2}\n{p*2}\n{p*2}\n{p*2}\n{p*2}"
        await e.edit(pay)
