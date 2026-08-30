from clients import mongo_db, LOGGER

users = mongo_db["users"] if mongo_db else None
chats = mongo_db["chats"] if mongo_db else None
settings = mongo_db["settings"] if mongo_db else None

async def add_user(user_id):
    if users:
        try:
            await users.update_one({"_id": user_id}, {"$set": {"_id": user_id}}, upsert=True)
        except Exception as e:
            LOGGER.warning("DB user error: %s", e)

async def add_chat(chat_id):
    if chats:
        try:
            await chats.update_one({"_id": chat_id}, {"$set": {"_id": chat_id}}, upsert=True)
        except Exception as e:
            LOGGER.warning("DB chat error: %s", e)

async def get_bot_status():
    if not settings:
        return True
    try:
        doc = await settings.find_one({"_id": "bot_status"})
        return True if not doc else bool(doc.get("enabled", True))
    except Exception:
        return True

async def set_bot_status(value):
    if settings:
        try:
            await settings.update_one(
                {"_id": "bot_status"},
                {"$set": {"enabled": bool(value)}},
                upsert=True,
            )
        except Exception as e:
            LOGGER.warning("DB status error: %s", e)


AUTOPLAY_KEY = "autoplay"

async def set_autoplay(chat_id: int, value: bool):
    if settings:
        try:
            await settings.update_one(
                {"_id": f"{AUTOPLAY_KEY}:{chat_id}"},
                {"$set": {"enabled": bool(value)}},
                upsert=True,
            )
        except Exception as e:
            LOGGER.warning("set_autoplay DB error: %s", e)

async def get_autoplay(chat_id: int) -> bool:
    if not settings:
        return False
    try:
        doc = await settings.find_one({"_id": f"{AUTOPLAY_KEY}:{chat_id}"})
        return bool(doc.get("enabled", False)) if doc else False
    except Exception as e:
        LOGGER.warning("get_autoplay DB error: %s", e)
        return False

async def _set_media(key: str, file_id: str, media_type: str):
    if settings:
        try:
            await settings.update_one(
                {"_id": key},
                {"$set": {"file_id": file_id, "media_type": media_type}},
                upsert=True,
            )
        except Exception as e:
            LOGGER.warning("set_media DB error: %s", e)

async def _get_media(key: str):
    if not settings:
        return None
    try:
        doc = await settings.find_one({"_id": key})
        return {"file_id": doc["file_id"], "media_type": doc["media_type"]} if doc else None
    except Exception as e:
        LOGGER.warning("get_media DB error: %s", e)
        return None

async def _delete_media(key: str):
    if settings:
        try:
            await settings.delete_one({"_id": key})
        except Exception as e:
            LOGGER.warning("delete_media DB error: %s", e)

async def set_start_media(file_id: str, media_type: str):
    await _set_media("start_media", file_id, media_type)

async def get_start_media():
    return await _get_media("start_media")

async def delete_start_media():
    await _delete_media("start_media")

async def set_group_start_media(file_id: str, media_type: str):
    await _set_media("group_start_media", file_id, media_type)

async def get_group_start_media():
    return await _get_media("group_start_media")

async def delete_group_start_media():
    await _delete_media("group_start_media")
