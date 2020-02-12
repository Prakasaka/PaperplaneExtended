#credit goes to Pru @Zero_cool7870 Sar

from telethon import events
import asyncio
from userbot.events import register
from userbot import bot


@register(outgoing=True, pattern="^.ttf (.*)")
async def get(event):
    name = event.text[5:]
    m = await event.get_reply_message()
    with open(name, "w") as f:
        f.write(m.message)
    await event.delete()
    await bot.send_file(event.chat_id,name,force_document=True)
	
             
             
             
