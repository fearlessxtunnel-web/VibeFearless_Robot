import logging
import time

from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client
from pytgcalls import PyTgCalls

import config

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pytgcalls").setLevel(logging.WARNING)

LOGGER = logging.getLogger("VibeFearless")
START_TIME = time.monotonic()

bot = Client(
    "VibeFearlessBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    in_memory=True,
)

assistant = Client(
    "FearlessAssistant",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.STRING_SESSION,
    in_memory=True,
)

call_py = PyTgCalls(assistant)

mongo_client = (
    AsyncIOMotorClient(config.MONGO_DB_URI)
    if config.MONGO_DB_URI else None
)
mongo_db = mongo_client["VibeFearless"] if mongo_client else None
