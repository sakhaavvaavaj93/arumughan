import asyncio
import importlib
from pytgcalls import PyTgCalls
import time
from pyrogram import Client
from arumughan import config

### Boot Time
boottime = time.time()

### auto
arumughan = Client(config.SESSION_NAME, config.API_ID, config.API_HASH)
pytgcalls = PyTgCalls(arumughan)

### Music Start Time
Music_START_TIME = time.time()

app = Client(
    "arumughan",
    config.API_ID,
    config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

client = Client(config.SESSION_NAME, config.API_ID, config.API_HASH)


app.start()
client.start()
all_info(app, client)
