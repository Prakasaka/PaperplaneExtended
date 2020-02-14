#This Lit Module By:- @Zero_cool7870 Sar
#Special thanks to @spechide who modified this aria

import aria2p
import asyncio
import os
from userbot import LOGS
from userbot.events import register


cmd = "aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800 --max-connection-per-server=10 --rpc-max-request-size=1024M --seed-time=0.01 --min-split-size=10M --follow-torrent=mem --split=10 --daemon=true --allow-overwrite=true"
EDIT_SLEEP_TIME_OUT = 5
aria2_is_running = os.system(cmd)

aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=6800,
            secret=""
        )
    )

 
        
@register(outgoing=True, pattern="^.magnet(?: |$)(.*)")
async def magnet_download(event):
    if event.fwd_from:
        return
    var = event.raw_text
    var = var.split(" ")
    magnet_uri = var[1]
    LOGS.info(magnet_uri)
    #Add Magnet URI Into Queue
    try:
        download = aria2.add_magnet(magnet_uri)
    except Exception as e:
        LOGS.info(str(e))
        await event.edit("Error:\n`" + str(e) + "`")
        return
    gid = download.gid
    await check_progress_for_dl(gid=gid,event=event,previous=None)
    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
    new_gid = await check_metadata(gid)
    await check_progress_for_dl(gid=new_gid,event=event,previous=None)
        
        
@register(outgoing=True, pattern="^.tor(?: |$)(.*)")
async def torrent_download(event):
    if event.fwd_from:
        return
    var = event.raw_text
    var = var.split(" ")
    torrent_file_path = var[1]
    torrent_file_path
    # Add Torrent Into Queue
    try:
        download = aria2.add_torrent(
            torrent_file_path,
            uris=None,
            options=None,
            position=None
        )
    except Exception as e:
        await event.edit(str(e))
        return
    gid = download.gid
    await check_progress_for_dl(gid=gid,event=event,previous=None)



@register(outgoing=True, pattern="^.url(?: |$)(.*)")
async def magnet_download(event):
    if event.fwd_from:
        return
    var = event.text[5:]
    print(var)  
    uris = [var]
    try: # Add URL Into Queue
        download = aria2.add_uris(uris, options=None, position=None)
    except Exception as e:
        LOGS.info(str(e))
        await event.edit("Error :\n`{}`".format(str(e)))
        return
    gid = download.gid
    await check_progress_for_dl(gid=gid,event=event,previous=None)
    file = aria2.get_download(gid)
    if file.followed_by_ids:
        new_gid = await check_metadata(gid)
        await progress_status(gid=new_gid,event=event,previous=None)

@register(outgoing=True, pattern="^.remove(?: |$)(.*)")
async def remove_all(event):
    if event.fwd_from:
        return
    try:
        removed = aria2.remove_all(force=True)
        aria2.purge_all()
    except:
        pass
    if removed == False:  # If API returns False Try to Remove Through System Call.
        os.system("aria2p remove-all")
    await event.edit("`Removing...`")
    await asyncio.sleep(2.5)
    await event.edit("`Removed`")
    await asyncio.sleep(2.5)
    await event.delete()


@register(outgoing=True, pattern="^.pause(?: |$)(.*)")
async def pause_all(event):
    if event.fwd_from:
        return
    # Pause ALL Currently Running Downloads.
    paused = aria2.pause_all(force=True)
    await event.edit("`Pausing Ur File...`")
    await asyncio.sleep(2.5)
    await event.edit("`Paused`")
    await asyncio.sleep(2.5)
    await event.delete()


@register(outgoing=True, pattern="^.resume(?: |$)(.*)")
async def resume_all(event):
    if event.fwd_from:
        return
    resumed = aria2.resume_all()
    await event.edit("`Resuming Ur File...`")
    await asyncio.sleep(1)
    await event.edit("`Resumed`")
    await asyncio.sleep(2.5)
    await event.delete()


@register(outgoing=True, pattern="^.show(?: |$)(.*)")
async def show_all(event):
    if event.fwd_from:
        return
    output = "output.txt"
    downloads = aria2.get_downloads() 
    msg = ""
    for download in downloads:
        msg = msg+"File: `"+str(download.name) +"`\nSpeed: "+ str(download.download_speed_string())+"\nProgress: "+str(download.progress_string())+"\nTotal Size: "+str(download.total_length_string())+"\nStatus: "+str(download.status)+"\nETA:  "+str(download.eta_string())+"\n\n"
    if len(msg) <= 4096:
        await event.edit("`Current Downloads: `\n"+msg)
        await asyncio.sleep(5)
        await event.delete()
    else:
        await event.edit("`Output is huge. Sending as a file...`")
        with open(output,'w') as f:
            f.write(msg)
        await asyncio.sleep(2)  
        await event.delete()    
        await borg.send_file(
            event.chat_id,
            output,
            force_document=True,
            supports_streaming=False,
            allow_cache=False,
            reply_to=event.message.id,
            )    
        
        
async def check_metadata(gid):
    file = aria2.get_download(gid)
    new_gid = file.followed_by_ids[0]
    LOGS.info("Changing GID "+ gid +" to" + new_gid)
    return new_gid


async def check_progress_for_dl(gid,event,previous):
    complete = None
    while not complete:
        file = aria2.get_download(gid)
        complete = file.is_complete
        try:
            if not file.error_message:
                msg = f"\nDownloading File: `{file.name}`"
                msg += f"\nSpeed: {file.download_speed_string()}"
                msg += f"\nProgress: {file.progress_string()}"
                msg += f"\nTotal Size: {file.total_length_string()}"
                msg += f"\nStatus: {file.status}"
                msg += f"\nETA: {file.eta_string()}"
                if msg != previous:
                    await event.edit(msg)
                    msg = previous     
            else:
                LOGS.info(str(file.error_message))
                await event.edit(f"`{msg}`")
            await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
            await check_progress_for_dl(gid,event,previous)
            file = aria2.get_download(gid)
            complete = file.is_complete
            if complete:
                await event.edit(f"File Downloaded Successfully:`{file.name}`")
                return False
        except Exception as e:
            if "not found" in str(e) or "'file'" in str(e):
                await event.edit("Download Canceled :\n`{}`".format(file.name))
                await asyncio.sleep(2.5)
                await event.delete()
                return
            elif " depth exceeded" in str(e):
                file.remove(force=True)
                await event.edit("Download Auto Canceled :\n`{}`\nYour Torrent/Link is Dead.".format(file.name))
