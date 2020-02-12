# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
# sp by peru @AvinashReddy3108 & @Zero_cool7870


""" Userbot module containing various scrapers. """

import os
import json
import asyncio
from time import sleep
from html import unescape
from datetime import datetime
from requests import get
from mtranslate import translate
from langdetect import detect
from youtube_dl import YoutubeDL
from youtube_dl.utils import (DownloadError, ContentTooShortError,
                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID
from userbot.events import register

LANG = "en"



@register(outgoing=True, pattern="^.yt (.*)")
async def yt_search(video_q):
    """ For .yt command, do a YouTube search from Telegram. """
    if not video_q.text[0].isalpha() and video_q.text[0] not in ("/", "#", "@",
                                                                 "!"):
        query = video_q.pattern_match.group(1)
        result = ''

        if not YOUTUBE_API_KEY:
            await video_q.edit(
                "`Error: YouTube API key missing! Add it to environment vars or config.env.`"
            )
            return

        await video_q.edit("```Processing...```")

        full_response = youtube_search(query)
        videos_json = full_response[1]

        for video in videos_json:
            title = f"{unescape(video['snippet']['title'])}"
            link = f"https://youtu.be/{video['id']['videoId']}"
            result += f"{title}\n{link}\n\n"

        reply_text = f"**Search Query:**: `{query}`\n\n{result}"

        await video_q.edit(reply_text)


def youtube_search(query,
                   order="relevance",
                   token=None,
                   location=None,
                   location_radius=None):
    """ Do a YouTube search. """
    youtube = build('youtube',
                    'v3',
                    developerKey=YOUTUBE_API_KEY,
                    cache_discovery=False)
    search_response = youtube.search().list(
        q=query,
        type="video",
        pageToken=token,
        order=order,
        part="id,snippet",
        maxResults=10,
        location=location,
        locationRadius=location_radius).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)
    try:
        nexttok = search_response["nextPageToken"]
        return (nexttok, videos)
    except HttpError:
        nexttok = "last_page"
        return (nexttok, videos)
    except KeyError:
        nexttok = "KeyError, try again."
        return (nexttok, videos)

# Thanks to @kandnub for parts of this code.
# Do check out his cool userbot at
# https://github.com/kandnub/TG-UserBot


@register(outgoing=True, pattern=r"^.trt(?: |$)([\s\S]*)")
async def message(trans):
    """ For .trt command, translate the given text using Google Translate. """
    if not trans.text[0].isalpha() and trans.text[0] not in ("/", "#", "@", "!"):
        target = (utils.arg_split_with(message, " ")) #Credit https://github.com/erenmetesar/NiceGrill/blob/master/nicegrill/modules/translate.py
        if not target:
            await message.edit("<i>Specify the target language.</i>")
            return
        if target and len(target) < 2 and not message.is_reply:
            await message.edit("<i>Specify the text to be translated.</i>")
            return
        reply = await message.get_reply_message()
        text = (
            target[1] if not message.is_reply else
            reply.text)
        target = target[0]
        if reply and not reply.text:
            await message.edit("<i>Babe..Are you okay? You can not translate files you know.</i>")
            return
        await message.edit("<i>Translating...</i>")
        result = translate(text, target, 'auto')
        await message.edit(
                           "<b>Text:</b> <i>{}</i>\n"
                           "<b>Detected Language:</b> <i>{}</i>\n\n"
                           "<b>Translated to:</b>\n<i>{}</i>"
                           .format(text, detect(text), result)) 
                  
CMD_HELP.update({
    'trt': '.trt <text> [or reply]\
        \nUsage: Translates text to the default language which is set.\nUse .lang <text> to set language for your TTS.'
})
CMD_HELP.update({
    'yt': '.yt <text>\
        \nUsage: Does a YouTube search.'
})
CMD_HELP.update({
    "imdb": ".imdb <movie-name>\nShows movie info and other stuffs"
})
