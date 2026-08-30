import asyncio
import threading

import aiohttp
import uvicorn
from fastapi import FastAPI
from pyrogram import idle
from pyrogram.types import BotCommand

import config
import db
import botstate
from clients import bot, assistant, call_py, LOGGER

import play  # noqa

web = FastAPI()

@web.get("/")
async def root():
    return {
        "status": "online",
        "bot": config.BOT_NAME,
        "assistant": config.ASSISTANT_NAME,
        "owner": f"@{config.OWNER_USERNAME}",
    }

@web.get("/health")
async def health():
    return {"ok": True}

def run_web():
    uvicorn.run(web, host="0.0.0.0", port=config.PORT, log_level="warning")

async def keep_alive():
    if not config.RENDER_EXTERNAL_URL:
        return
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(
                    config.RENDER_EXTERNAL_URL,
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as response:
                    LOGGER.info("Keep-alive: %s", response.status)
            except Exception as e:
                LOGGER.warning("Keep-alive failed: %s", e)
            await asyncio.sleep(config.PING_INTERVAL)

async def register_commands():
    commands = [
        BotCommand("start", "Open Vibe Fearless"),
        BotCommand("play", "Search and play music"),
        BotCommand("queue", "Show music queue"),
        BotCommand("nowplaying", "Current track"),
        BotCommand("pause", "Pause playback"),
        BotCommand("resume", "Resume playback"),
        BotCommand("skip", "Skip current track"),
        BotCommand("stop", "Stop and leave VC"),
        BotCommand("shuffle", "Shuffle queue"),
        BotCommand("loop", "Toggle loop"),
        BotCommand("autoplay", "Toggle autoplay"),
        BotCommand("volume", "Set volume"),
        BotCommand("stats", "Bot status"),
        BotCommand("help", "Command list"),
    ]
    try:
        await bot.set_bot_commands(commands)
    except Exception as e:
        LOGGER.warning("Command registration failed: %s", e)

async def start_all():
    await bot.start()
    LOGGER.info("Bot started")
    await assistant.start()
    LOGGER.info("Assistant started")

    # Warm Telegram peer cache; this reduces late Peer-id failures.
    try:
        async for _ in assistant.get_dialogs():
            pass
        LOGGER.info("Assistant dialogs cached")
    except Exception as e:
        LOGGER.warning("Dialog cache warning: %s", e)

    await call_py.start()
    LOGGER.info("PyTgCalls started")

    botstate.set_enabled(await db.get_bot_status())
    await register_commands()

    if config.LOG_GROUP_ID:
        try:
            await bot.send_message(
                config.LOG_GROUP_ID,
                "🟢 <b>VIBE FEARLESS</b> is online.\n"
                f"🎧 {config.ASSISTANT_NAME}\n"
                f"👑 @{config.OWNER_USERNAME}",
            )
        except Exception as e:
            LOGGER.warning("Log group message failed: %s", e)

async def main():
    while True:
        try:
            await start_all()
            task = asyncio.create_task(keep_alive())
            try:
                await idle()
            finally:
                task.cancel()
            break
        except Exception as e:
            LOGGER.exception("Main loop crashed: %s", e)
            await asyncio.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(main())
