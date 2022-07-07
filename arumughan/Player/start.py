import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import MessageNotModified
from arumughan.main import Test, bot as Client



from arumughan.Database.dbusers import add_served_user
from config import START_PIC, UPDATES_CHANNEL, GROUP_SUPPORT


ALIVE_PIC = START_PIC

HOME_TEXT = """
𝙸 𝚊𝚖 𝚊 𝚕𝚊𝚐𝚐𝚕𝚎𝚜𝚜 𝚖𝚞𝚜𝚒𝚌 𝚋𝚘𝚝 𝚌𝚛𝚎𝚊𝚝𝚎𝚍 𝚏𝚘𝚛 [കണിമംഗലം](https://t.me/kk_kovilakam)
"""
HELP_TEXT = """
✘ **ʜᴏᴡ ᴛᴏ ꜱᴇᴛᴜᴘ?**

‣ ꜱᴛᴀʀᴛ ᴀ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ.
‣ ᴀᴅᴅ ʙᴏᴛ `{}` ᴀɴᴅ ᴜꜱᴇʀ ᴀᴄᴄᴏᴜɴᴛ ɪɴ ᴄʜᴀᴛ ᴡɪᴛʜ ᴀᴅᴍɪɴ ʀɪɢʜᴛꜱ.
‣ ᴅᴏɴᴇ ꜱᴇᴛᴜᴘ ᴘʀᴏᴄᴇꜱꜱ ʀᴇᴀᴅ ᴄᴏᴍᴍᴀɴᴅꜱ ʙᴇʟᴏᴡ 👇.
"""



USER_TEXT = """
✘ **ᴜꜱᴇʀꜱ ᴄᴏᴍᴍᴀɴᴅꜱ** 

‣ /play <Qᴜᴇʀʏ> ᴛᴏ ᴘʟᴀʏ ᴀ ꜱᴏɴɢ.
‣ /vplay <Qᴜᴇʀʏ> ᴛᴏ ᴘʟᴀʏ ᴠɪᴅᴇᴏ.
‣ /stream <ʟɪᴠᴇ ᴜʀʟ> ᴛᴏ ᴘʟᴀʏ ʟɪᴠᴇ ꜱᴛʀᴇᴀᴍꜱ.
‣ /song ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴀ ᴀᴜᴅɪᴏ ꜰɪʟᴇ ꜰʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ. 
‣ /video ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏ ꜰʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ.
‣ /lyric ᴛᴏ ꜰɪɴᴅ ʟʏʀɪᴄꜱ.
"""

ADMIN = """
✘ **ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅꜱ** :

‣ /changeassistant <1,2,3,4,5> ᴛᴏ ᴄʜᴀɴɢᴇ ᴀꜱꜱɪꜱᴛᴀɴᴛ (ɪꜰ 2 ᴏʀ ᴍᴏʀᴇ ᴀꜱꜱɪꜱᴛᴀɴᴛ<ᴍᴜʟᴛɪ ᴀꜱꜱɪꜱᴛᴀɴᴛ>).
‣ /checkassistant ᴛᴏ ᴄʜᴇᴄᴋ ᴡʜɪᴄʜ ᴀꜱꜱɪꜱᴛᴀɴᴛ ᴘʀᴇꜱᴇɴᴛ ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ.
‣ /end ᴛᴏ ᴇɴᴅ ꜱᴛʀᴇᴀᴍɪɴɢ.
‣ /pause ᴛᴏ ᴘᴀᴜꜱᴇ ꜱᴛʀᴇᴀᴍ.
‣ /resume ᴛᴏ ʀᴇꜱᴜᴍᴇ ꜱᴛʀᴇᴀᴍ.
‣ /volume ᴛᴏ ꜱᴇᴛ ᴠᴏʟᴜᴍᴇ.
‣ /skip ᴛᴏ ꜱᴋɪᴘ ᴛʀᴀᴄᴋꜱ.
"""

SUDO_TEXT = """
✘ **ꜱᴏᴍᴇ ᴍᴏʀᴇ ᴇxᴛʀᴀ ᴄᴏᴍᴍᴀɴᴅꜱ ꜰᴏʀ ꜱᴜᴅᴏ ᴜꜱᴇʀꜱ**

‣ /gban ᴛᴏ ʙᴀɴ ꜱᴏᴍᴇᴏɴᴇ ɢʟᴏʙᴀʟʟʏ.
‣ /ungban ᴛᴏ ᴜɴʙᴀɴ  ɢʟᴏʙᴀʟʟʏ ɪꜰ ɢʙᴀɴɴᴇᴅ.
‣ /broadcast ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴡʜɪᴄʜ ᴘʀᴇꜱᴇɴᴛ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀꜱᴇ.
‣ /activevoice ᴛᴏ ᴄʜᴇᴄᴋ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛꜱ.
‣ /activevideo ᴛᴏ ᴄʜᴇᴄᴋ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛꜱ.
"""

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data=="help":
        get_me = await client.get_me()
        USERNAME = get_me.username
        buttons = [
            [
                InlineKeyboardButton("✘ ᴀᴅᴍɪɴꜱ", callback_data="azminss"),
                InlineKeyboardButton("✘ ᴜꜱᴇʀꜱ", callback_data="users"),
            ],
            [
                InlineKeyboardButton("✘ Bᴀᴄᴋ", callback_data="home"),
                InlineKeyboardButton("✘ Cʟᴏꜱᴇ", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HELP_TEXT.format(USERNAME),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="home":
        get_me = await client.get_me()
        USERNAME = get_me.username
        buttons = [
            [
                InlineKeyboardButton("✘ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛꜱ", url='https://t.me/{USERNAME}?startgroup=true'),
            ],
            [
                InlineKeyboardButton("✘ ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton("✘ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"),
            ],
            [
                InlineKeyboardButton("✘ ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅꜱ", callback_data="help"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HOME_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="users":
        buttons = [
            [
                InlineKeyboardButton("✘ Bᴀᴄᴋ", callback_data="help"),
                InlineKeyboardButton("✘ Cʟᴏꜱᴇ", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                USER_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass
    elif query.data=="azminss":
        buttons = [
            [
                InlineKeyboardButton("✘ Bᴀᴄᴋ", callback_data="help"),
                InlineKeyboardButton("✘ Cʟᴏꜱᴇ", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                ADMIN,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass

    elif query.data=="cls":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass


@Client.on_message(filters.command(["start"]) & filters.private)
async def start(client: Client, message: Message):
    get_me = await client.get_me()
    user_id = message.from_user.id
    await add_served_user(user_id)
    USERNAME = get_me.username
    buttons = [
            [
                InlineKeyboardButton("✘ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛꜱ", url='https://t.me/{USERNAME}?startgroup=true'),
            ],
            [
                InlineKeyboardButton("✘ ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton("✘ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"),
            ],
            [
                InlineKeyboardButton("✘ ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅꜱ", callback_data="help"),
            ]
            ]     
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_photo(photo=f"{ALIVE_PIC}", caption=HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)

@Client.on_message(filters.command(["help"]) & filters.private)
async def help(client: Client, message: Message):
    get_me = await client.get_me()
    self.username = get_me.username
    buttons = [
           [
                InlineKeyboardButton("✘ ᴀᴅᴍɪɴꜱ", call_back_data="azminss"),
                InlineKeyboardButton("✘ ᴜꜱᴇʀꜱ", callback_data="users"),
            ],
