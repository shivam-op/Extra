from telethon.errors.rpcerrorlist import UserIdInvalidError, MessageTooLongError
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest, EditPhotoRequest
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import ChannelParticipantsAdmins, ChatAdminRights, ChatBannedRights, MessageEntityMentionName, MessageMediaPhoto
from . import *


async def get_full_user(event):  
    args = event.pattern_match.group(1).split(':', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await eor(event, "Need a user to do this...")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await eor(event, f"**ERROR !!**\n\n`{str(err)}`")           
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj



@bot.on(hell_cmd(pattern="gpro ?(.*)"))
@bot.on(sudo_cmd(pattern="gpro ?(.*)", allow_sudo=True))
async def _(hellevent):
    i = 0
    sender = await hellevent.get_sender()
    me = await hellevent.client.get_me()
    hell = await eor(hellevent, "`Promoting globally...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await hellevent.get_chat()
    if hellevent.is_private:
        user = hellevent.chat
        rank = hellevent.pattern_match.group(1)
    else:
        hellevent.chat.title
    try:
        user, rank = await get_full_user(hellevent)
    except:
        pass
    if me == user:
       k = await hell.edit("You can't promote yourself...")
       return
    try:
        if not rank:
            rank = "ㅤ"
    except:
        return await hell.edit("**ERROR !!**")
    if user:
        telchanel = [d.entity.id
                     for d in await hellevent.client.get_dialogs()
                     if (d.is_group or d.is_channel)
                     ]
        rgt = ChatAdminRights(add_admins=False,
                               invite_users=True,
                                change_info=False,
                                 ban_users=True,
                                  delete_messages=True,
                                   pin_messages=True)
        for x in telchanel:
          try:
             await hellevent.client(EditAdminRequest(x, user, rgt, rank))
             i += 1
             await hell.edit(f"**Promoting User in :**  `{i}` Chats...")
          except:
             pass
    else:
        await hell.edit(f"**Reply to a user !!**")
    await hell.edit(
        f"[{user.first_name}](tg://user?id={user.id}) **Was Promoted Globally In** `{i}` **Chats !!**"
    )
    await bot.send_message(Config.LOGGER_ID, f"#GPROMOTE \n\n**Globally Promoted User :** [{user.first_name}](tg://user?id={user.id}) \n\n**Total Chats :** `{i}`")


@bot.on(hell_cmd(pattern="gdem ?(.*)"))
@bot.on(sudo_cmd(pattern="gdem ?(.*)", allow_sudo=True))
async def _(hellevent):
    i = 0
    sender = await hellevent.get_sender()
    me = await hellevent.client.get_me()
    hell = await eor(hellevent, "`Demoting Globally...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await hellevent.get_chat()
    if hellevent.is_private:
        user = hellevent.chat
        rank = hellevent.pattern_match.group(1)
    else:
        hellevent.chat.title
    try:
        user, rank = await get_full_user(hellevent)
    except:
        pass
    if me == user:
       k = await hell.edit("You can't Demote yourself !!")
       return
    try:
        if not rank:
            rank = "ㅤ"
    except:
        return await hell.edit("**ERROR !!**")
    if user:
        telchanel = [d.entity.id
                     for d in await hellevent.client.get_dialogs()
                     if (d.is_group or d.is_channel)
                     ]
        rgt = ChatAdminRights(add_admins=None,
                               invite_users=None,
                                change_info=None,
                                 ban_users=None,
                                  delete_messages=None,
                                   pin_messages=None)
        for x in telchanel:
          try:
             await hellevent.client(EditAdminRequest(x, user, rgt, rank))
             i += 1
             await hell.edit(f"**Demoting Globally In Chats :** `{i}`")
          except:
             pass
    else:
        await hell.edit(f"**Reply to a user !!**")
    await hell.edit(
        f"[{user.first_name}](tg://user?id={user.id}) **Was Demoted Globally In** `{i}` **Chats !!**"
    )
    await bot.send_message(Config.LOGGER_ID, f"#GDEMOTE \n\n**Globally Demoted :** [{user.first_name}](tg://user?id={user.id}) \n\n**Total Chats :** `{i}`")