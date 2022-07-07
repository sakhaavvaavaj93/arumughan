#None

active = []
activevideo = []
arumughan = []

async def get_active_chats() -> list:
    return active


async def is_active_chat(chat_id: int) -> bool:
    if chat_id not in active:
        return False
    else:
        return True


async def add_active_chat(chat_id: int):
    if chat_id not in active:
        active.append(chat_id)

async def remove_active_chat(chat_id: int):
    if chat_id in active:
        active.remove(chat_id)

# Raids
async def get_raid_chats() -> list:
    return arumughan

async def add_raid_chat(chat_id: int):
    if chat_id not in arumughan:
        arumughan.append(chat_id)

async def remove_raid_chat(chat_id: int):
    if chat_id in arumughan:
        arumughan.remove(chat_id)




# Active Video Chats
async def get_active_video_chats() -> list:
    return activevideo


async def is_active_video_chat(chat_id: int) -> bool:
    if chat_id not in activevideo:
        return False
    else:
        return True


async def add_active_video_chat(chat_id: int):
    if chat_id not in activevideo:
        activevideo.append(chat_id)


async def remove_active_video_chat(chat_id: int):
    if chat_id in activevideo:
        activevideo.remove(chat_id)
