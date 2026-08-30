import os

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")

OWNER_ID = int(os.getenv("OWNER_ID", "0"))
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "0"))

MONGO_DB_URI = os.getenv("MONGO_DB_URI", "")
PORT = int(os.getenv("PORT", "10000"))

BOT_NAME = "Vibe Fearless"
ASSISTANT_NAME = "FEARLESS ASSISTANT"
OWNER_USERNAME = "Fearless45op"
CHANNEL_USERNAME = "SPARK_X_NETWORK_OP"
GROUP_USERNAME = "SPARK_X_NETWORK"

OWNER_URL = f"https://t.me/{OWNER_USERNAME}"
CHANNEL_URL = f"https://t.me/{CHANNEL_USERNAME}"
GROUP_URL = f"https://t.me/{GROUP_USERNAME}"

ASSISTANT_USERNAME = os.getenv("ASSISTANT_USERNAME", "")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "")
PING_INTERVAL = int(os.getenv("PING_INTERVAL", "600"))

MAX_QUEUE = int(os.getenv("MAX_QUEUE", "50"))
SEARCH_TIMEOUT = int(os.getenv("SEARCH_TIMEOUT", "20"))
STREAM_TIMEOUT = int(os.getenv("STREAM_TIMEOUT", "25"))
DEFAULT_VOLUME = int(os.getenv("DEFAULT_VOLUME", "100"))
MAX_VOLUME = int(os.getenv("MAX_VOLUME", "200"))

SUPPORT_URL = GROUP_URL

API_KEY = os.getenv("API_KEY", "")
API_URL = os.getenv("API_URL", "")
API_TYPE = os.getenv("API_TYPE", "audio")
API_FORMAT = os.getenv("API_FORMAT", "mp3")
