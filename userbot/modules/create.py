#this module originally created by @spechide https://github.com/SpEcHiDe/UniBorg/blob/master/stdplugins/create_private_group.py


from telethon.tl import functions, types
from userbot.events import register
from userbot import CMD_HELP


@register(outgoing=True, pattern="^.create (c|g)(?: |$)(.*)")
async def telegraphs(grop):
    """ For .create command, Creating New Group & Channel """
    if not grop.text[0].isalpha() and grop.text[0] not in ("/", "#", "@", "!"):
        if grop.fwd_from:
            return
        type_of_group = grop.pattern_match.group(1)
        group_name = grop.pattern_match.group(2)
        if type_of_group == "g":
            try:
                r = await grop.client(functions.channels.CreateChannelRequest(  # pylint:disable=E0602
                    title=group_name,
                    about="Welcome",
                    megagroup=True
                ))
                created_chat_id = r.chats[0].id
                result = await grop.client(functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                ))
                await grop.edit(f"**SuperGroup Created Successfully.\nSuperGroup : ** [{group_name}]({result.link})")
            except Exception as e:  # pylint:disable=C0103,W0703
                await grop.edit(str(e))
        elif type_of_group == "c":
            try:
                r = await grop.client(functions.channels.CreateChannelRequest(  # pylint:disable=E0602
                    title=group_name,
                    about="Welcome",
                    megagroup=False
                ))
                created_chat_id = r.chats[0].id
                result = await grop.client(functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                ))
                await grop.edit(f"**Channel Created Successfully.\nChannel : ** [{group_name}]({result.link})")
            except Exception as e:  # pylint:disable=C0103,W0703
                await grop.edit(str(e))
        else:
            await grop.edit("**Wrong Character. Type g for SuperGroup or c for Channel**")

CMD_HELP.update({
    "create": "\
Create\
\nUsage: Create Channel & SuperGroup.\
\n\n.create c\
\nUsage: Create a Channel.\
\n\n.create g\
\nUsage: Create a Private Group.\
"})
