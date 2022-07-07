# @kk_kovilakam
import io
from os import path
from typing import Callable
from asyncio.queues import QueueEmpty
import os
import random
import re
from random import choice
import aiofiles
import aiohttp
from arumughan.converter import convert
from Process.design.thumbnail import *
import ffmpeg
import requests
from arumughan.fonts import CHAT_TITLE
from PIL import Image, ImageDraw, ImageFont
from config import ASSISTANT_NAME, BOT_USERNAME, QUE_IMG, CMD_IMG, PLAY_IMG, UPDATES_CHANNEL, GROUP_SUPPORT
from arumughan.filters import command, other_filters
from arumughan.queues import QUEUE, add_to_queue
from arumughan.main import call_py, Test as user, call_py2, call_py3, call_py4, call_py5
from arumughan.utils import bash
from arumughan.main import bot as Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch
from arumughan.Database.clientdb import * 
from arumughan.Client.assistant import get_assistant_details, random_assistant
from arumughan.Client.Joiner import AssistantAdd
from arumughan.Database.active import *
from arumughan.Database.dbchat import add_served_chat, is_served_chat

import yt_dlp
import yt_dlp


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        videoid = data["id"]
        return [songname, url, duration, thumbnail, videoid]
    except Exception as e:
        print(e)
        return 0


async def ytdl(format: str, link: str):
    stdout, stderr = await bash(f'yt-dlp --geo-bypass -g -f "[height<=?720][width<=?1280]" {link}')
    if stdout:
        return 1, stdout
    return 0, stderr

chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
ACTV_CALLS = []




def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", 
        format="s16le", 
        acodec="pcm_s16le", 
        ac=2, 
        ar="48k"
    ).overwrite_output().run()
    os.remove(filename)

def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))
    
@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
@AssistantAdd
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    _assistant = await get_assistant(chat_id, "assistant")
    assistant = _assistant["saveassistant"]
    
    if m.sender_chat:
        return await m.reply_text("you're an __Anonymous__ Admin !\n\n» revert back to user account from admin rights.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 To use me, I need to be an **Administrator** with the following **permissions**:\n\n» ❌ __Delete messages__\n» ❌ __Add users__\n» ❌ __Manage video chat__\n\nData is **updated** automatically after you **promote me**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "missing required permission:" + "\n\n» ❌ __Manage video chat__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "missing required permission:" + "\n\n» ❌ __Delete messages__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("missing required permission:" + "\n\n» ❌ __Add users__")
        return
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 **downloading audio...**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else:
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_text(
                    f"💡 **Track added to queue »** `{pos}`",
                )
            else:
             try:
                if int(assistant) == 1:
                   await call_py.join_group_call(
                       chat_id,
                       AudioPiped(
                           dl,
                       ),
                       stream_type=StreamType().local_stream,
                   )
                if int(assistant) == 2:
                   await call_py2.join_group_call(
                       chat_id,
                       AudioPiped(
                           dl,
                       ),
                       stream_type=StreamType().local_stream,
                   )
                if int(assistant) == 3:
                   await call_py3.join_group_call(
                       chat_id,
                       AudioPiped(
                           dl,
                       ),
                       stream_type=StreamType().local_stream,
                   )
                if int(assistant) == 4:
                   await call_py4.join_group_call(
                       chat_id,
                       AudioPiped(
                           dl,
                       ),
                       stream_type=StreamType().local_stream,
                   )
                if int(assistant) == 5:
                   await call_py5.join_group_call(
                       chat_id,
                       AudioPiped(
                           dl,
                       ),
                       stream_type=StreamType().local_stream,
                   )
                await add_active_chat(chat_id)
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_text(
                    f"Playing**[{songname}]",
                )
             except Exception as e:
                await suhu.delete()
                await m.reply_text(f"🚫 error:\n\n» {e}")
        
    else:
        if len(m.command) < 2:
         await m.reply_photo(
                     photo=f"{CMD_IMG}",
                    caption="💬**Usage: /play Give a Title Song To Play Music or /vplay for Video Play**"
                    ,
                      reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🗑 Close", callback_data="cls")
                        ]
                    ]
                )
            )
        else:
            suhu = await m.reply_text(
        f"**Downloading**\n\n0% ▓▓▓▓▓▓▓▓▓▓▓▓ 100%"
    )
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("💬 **no results found.**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                videoid = search[4]
                userid = m.from_user.id
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                image = await play_thumb(videoid)
                queuem = await queue_thumb(videoid)
                format = "bestaudio"
                abhi, ytlink = await ytdl(format, url)
                if abhi == 0:
                    await suhu.edit(f"💬 yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_text(
                            f"💡 **Track added to queue »** `{pos}`",
                        )
                    else:
                        try:
                            await suhu.edit(
                            f"**Downloader**\n\n**Title**: {title[:22]}\n\n100% ████████████100%\n\n**Time Taken**: 00:00 Seconds\n\n**Converting Audio[FFmpeg Process]**"
                        )
                            if int(assistant) == 1:
                               await call_py.join_group_call(
                                   chat_id,
                                   AudioPiped(
                                       ytlink,
                                   ),
                                   stream_type=StreamType().local_stream,
                               )
                            if int(assistant) == 2:
                               await call_py2.join_group_call(
                                   chat_id,
                                   AudioPiped(
                                       ytlink,
                                   ),
                                   stream_type=StreamType().local_stream,
                               )
                            if int(assistant) == 3:
                               await call_py3.join_group_call(
                                   chat_id,
                                   AudioPiped(
                                       ytlink,
                                   ),
                                   stream_type=StreamType().local_stream,
                               )
                            if int(assistant) == 4:
                               await call_py4.join_group_call(
                                   chat_id,
                                   AudioPiped(
                                       ytlink,
                                   ),
                                   stream_type=StreamType().local_stream,
                               )
                            if int(assistant) == 5:
                               await call_py5.join_group_call(
                                   chat_id,
                                   AudioPiped(
                                       ytlink,
                                   ),
                                   stream_type=StreamType().local_stream,
                               )
                            if int(assistant) == 6:
                               await call_py.join_group_call(
                                   chat_id,
                                   AudioPiped(
                                       ytlink,
                                   ),
                                   stream_type=StreamType().local_stream,
                               )
                            await add_active_chat(chat_id)
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            await m.reply_text(
                                f"🏷 **𝚙𝚕𝚊𝚢𝚒𝚗𝚐**[{songname[:22]}]",
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"💬 error: `{ep}`")
                   elif type_ == "skip":
        if qeue:
            qeue.pop(0)
        if chet_id not in callsmusic.active_chats:
            await cb.answer("Chat is not connected!", show_alert=True)
        else:
            queues.task_done(chet_id)
            if queues.is_empty(chet_id):
                callsmusic.stop(chet_id)
                await cb.message.edit("- No More Playlist..\n- Leaving VC!")
            else:
                await callsmusic.set_stream(
                    chet_id, queues.get(chet_id)["file"]
                )
                await cb.answer.reply_text("✅ <b>Skipped</b>")
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text(
                    f"- Skipped track\n- Now Playing **{qeue[0][0]}**"
                )
