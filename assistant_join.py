from pyrogram.errors import (
    UserNotParticipant, UserAlreadyParticipant, FloodWait,
    ChatAdminRequired, RPCError,
)
from clients import bot, assistant, LOGGER

async def is_assistant_in_chat(chat_id):
    try:
        await assistant.get_chat_member(chat_id, "me")
        return True
    except UserNotParticipant:
        return False
    except Exception as e:
        LOGGER.warning("Assistant membership check: %s", e)
        return False

async def ensure_assistant_in_chat(chat_id):
    if await is_assistant_in_chat(chat_id):
        return True, ""

    chat = None
    try:
        chat = await bot.get_chat(chat_id)
    except Exception as e:
        LOGGER.warning("get_chat failed: %s", e)

    if chat and chat.username:
        try:
            await assistant.join_chat(chat.username)
            return True, ""
        except UserAlreadyParticipant:
            return True, ""
        except FloodWait as e:
            return False, f"FloodWait:{e.value}"
        except RPCError:
            pass

    try:
        link = getattr(chat, "invite_link", None)
        if not link:
            link = await bot.export_chat_invite_link(chat_id)
        if link:
            try:
                await assistant.join_chat(link)
                return True, ""
            except UserAlreadyParticipant:
                return True, ""
    except ChatAdminRequired:
        pass
    except FloodWait as e:
        return False, f"FloodWait:{e.value}"
    except Exception as e:
        LOGGER.warning("Invite join failed: %s", e)

    try:
        me = await assistant.get_me()
        await bot.add_chat_members(chat_id, me.id)
        if await is_assistant_in_chat(chat_id):
            return True, ""
    except Exception as e:
        LOGGER.warning("Bot add assistant failed: %s", e)

    return False, "manual_needed"
