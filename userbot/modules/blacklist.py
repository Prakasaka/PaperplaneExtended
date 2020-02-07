# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import asyncio
import re
import userbot.modules.sql_helper.blacklist_sql as sql
from io import BytesIO
from telethon import events, utils
from telethon.tl import types, functions
from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register


@register(incoming=True, disable_edited=True)
async def on_new_message(event):
    # TODO: exempt admins from locks
    name = event.raw_text
    snips = sql.get_chat_blacklist(event.chat_id)
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            try:
                await event.delete()
            except Exception as e:
                await event.reply("I do not have DELETE permission in this chat")
                sql.rm_from_blacklist(event.chat_id, snip.lower())
            break


@register(outgoing=True, pattern="^.addblacklist ((.|\n)*)")
async def on_add_black_list(event):
    text = event.pattern_match.group(1)
    to_blacklist = list(set(trigger.strip() for trigger in text.split("\n") if trigger.strip()))
    for trigger in to_blacklist:
        sql.add_to_blacklist(event.chat_id, trigger.lower())
    await event.edit("Added {} triggers to the blacklist in the current chat".format(len(to_blacklist)))

# Announce to the logging group if we have successfully Added a blacklist.
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#BLACKLIST\n"
            f"TRIGGER: {trigger}\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)"
        )


@register(outgoing=True, pattern="^.blacklist(.*)")
async def on_view_blacklist(event):
    all_blacklisted = sql.get_chat_blacklist(event.chat_id)
    OUT_STR = "Blacklists in the Current Chat:\n"
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f"👉 {trigger} \n"
    else:
        OUT_STR = "No BlackLists. Start Saving using `.addblacklist`"    
    await event.edit(OUT_STR)


@register(outgoing=True, pattern="^.rmblacklist ((.|\n)*)")
async def on_delete_blacklist(event):
    text = event.pattern_match.group(1)
    to_unblacklist = list(set(trigger.strip() for trigger in text.split("\n") if trigger.strip()))
    successful = 0
    for trigger in to_unblacklist:
        if sql.rm_from_blacklist(event.chat_id, trigger.lower()):
            successful += 1
    await event.edit(f"Removed {successful} / {len(to_unblacklist)} from the blacklist")

# Announce to the logging group if we have removed a blacklist successfully
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#RMBLACKLIST\n"
            f"TRIGGER: {trigger}\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)"
        )
