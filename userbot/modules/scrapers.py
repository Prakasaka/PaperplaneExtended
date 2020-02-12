# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
# sp by peru @AvinashReddy3108 & @Zero_cool7870


""" Userbot module containing various scrapers. """

import os
import shutil
from bs4 import BeautifulSoup
import re
import json
import asyncio
from time import sleep
from html import unescape
from datetime import datetime
from requests import get
from googletrans import LANGUAGES, Translator
from mtranslate import translate
from langdetect import detect
from gtts import gTTS
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




@register(outgoing=True, pattern="^.imdb (.*)")
async def imdb(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        try:
            movie_name = e.pattern_match.group(1)
            remove_space = movie_name.split(' ')
            final_name = '+'.join(remove_space)
            page = get("https://www.imdb.com/find?ref_=nv_sr_fn&q="+final_name+"&s=all")
            lnk = str(page.status_code)
            soup = BeautifulSoup(page.content,'lxml')
            odds = soup.findAll("tr","odd")
            mov_title = odds[0].findNext('td').findNext('td').text
            mov_link = "http://www.imdb.com/"+odds[0].findNext('td').findNext('td').a['href']
            page1 = get(mov_link)
            soup = BeautifulSoup(page1.content,'lxml')
            if soup.find('div','poster'):
    	        poster = soup.find('div','poster').img['src']
            else:
    	        poster = ''
            if soup.find('div','title_wrapper'):
    	        pg = soup.find('div','title_wrapper').findNext('div').text
    	        mov_details = re.sub(r'\s+',' ',pg)
            else:
    	        mov_details = ''
            credits = soup.findAll('div', 'credit_summary_item')
            if len(credits)==1:
    	        director = credits[0].a.text
    	        writer = 'Not available'
    	        stars = 'Not available'
            elif len(credits)>2:
    	        director = credits[0].a.text
    	        writer = credits[1].a.text
    	        actors = []
    	        for x in credits[2].findAll('a'):
    		        actors.append(x.text)
    	        actors.pop()
    	        stars = actors[0]+','+actors[1]+','+actors[2]
            else:
    	        director = credits[0].a.text
    	        writer = 'Not available'
    	        actors = []
    	        for x in credits[1].findAll('a'):
    		        actors.append(x.text)
    	        actors.pop()
    	        stars = actors[0]+','+actors[1]+','+actors[2]
            if soup.find('div', "inline canwrap"):
    	        story_line = soup.find('div', "inline canwrap").findAll('p')[0].text
            else:
    	        story_line = 'Not available'
            info = soup.findAll('div', "txt-block")
            if info:
    	        mov_country = []
    	        mov_language = []
    	        for node in info:
    		        a = node.findAll('a')
    		        for i in a:
    			        if "country_of_origin" in i['href']:
    				        mov_country.append(i.text)
    			        elif "primary_language" in i['href']:
    				        mov_language.append(i.text)
            if soup.findAll('div',"ratingValue"):
    	        for r in soup.findAll('div',"ratingValue"):
    		        mov_rating = r.strong['title']
            else:
    	        mov_rating = 'Not available'
            await e.edit('<a href='+poster+'>&#8203;</a>'
    			        '<b>Title : </b><code>'+mov_title+
    			        '</code>\n<code>'+mov_details+
    			        '</code>\n<b>Rating : </b><code>'+mov_rating+
    			        '</code>\n<b>Country : </b><code>'+mov_country[0]+
    			        '</code>\n<b>Language : </b><code>'+mov_language[0]+
    			        '</code>\n<b>Director : </b><code>'+director+
    			        '</code>\n<b>Writer : </b><code>'+writer+
    			        '</code>\n<b>Stars : </b><code>'+stars+
    			        '</code>\n<b>IMDB Url : </b>'+mov_link+
    			        '\n<b>Story Line : </b>'+story_line,
    			        link_preview = True , parse_mode = 'HTML'
    			        )
        except IndexError:
            await e.edit("Plox enter **Valid movie name** kthx")

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
