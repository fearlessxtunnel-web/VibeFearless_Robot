from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helpers import esc, duration, progress
import music_queue as mq
import config

def start_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎵 Play Music", callback_data="help_play"),
            InlineKeyboardButton("📖 Commands", callback_data="help"),
        ],
        [
            InlineKeyboardButton("📢 Channel", url=config.CHANNEL_URL),
            InlineKeyboardButton("👥 Group", url=config.GROUP_URL),
        ],
        [InlineKeyboardButton("⚡ Owner", url=config.OWNER_URL)],
    ])

def player_keyboard(chat_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏸ Pause", callback_data=f"pause:{chat_id}"),
            InlineKeyboardButton("▶️ Resume", callback_data=f"resume:{chat_id}"),
            InlineKeyboardButton("⏭ Skip", callback_data=f"skip:{chat_id}"),
        ],
        [
            InlineKeyboardButton("📜 Queue", callback_data=f"queue:{chat_id}"),
            InlineKeyboardButton("🔀 Shuffle", callback_data=f"shuffle:{chat_id}"),
            InlineKeyboardButton("⏹ Stop", callback_data=f"stop:{chat_id}"),
        ],
        [
            InlineKeyboardButton("🔉 Vol −", callback_data=f"vol:{chat_id}:down"),
            InlineKeyboardButton("🔊 Vol +", callback_data=f"vol:{chat_id}:up"),
            InlineKeyboardButton("🔁 Loop", callback_data=f"loop:{chat_id}"),
        ],
        [InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh:{chat_id}")],
    ])

def now_playing(chat_id, current=0):
    track = mq.now(chat_id)
    if not track:
        return "<b>🎵 Nothing is playing.</b>"
    total = int(track.get("duration") or 0)
    cur = int(current or 0)
    status = "⏸ PAUSED" if mq.state(chat_id) == "paused" else "▶️ PLAYING"
    return (
        f"<b>🎧 NOW PLAYING</b>\n"
        f"{'━' * 24}\n"
        f"🎵 <b>{esc(track.get('title'))}</b>\n"
        f"👤 Requested by {track.get('requested_by','Unknown')}\n"
        f"⏱ <code>{duration(cur)} / {duration(total)}</code>\n"
        f"<code>{progress(cur,total)}</code>\n"
        f"🔊 <b>{mq.volume(chat_id)}%</b>  •  {status}\n"
        f"{'━' * 24}\n"
        f"<i>Vibe Fearless • FEARLESS ASSISTANT</i>"
    )

def queue_text(chat_id):
    q = mq.queue(chat_id)
    if not q:
        return "<b>📜 Queue is empty.</b>"
    lines = ["<b>📜 VIBE FEARLESS QUEUE</b>", ""]
    for i, track in enumerate(q[:20], 1):
        lines.append(f"{i}. 🎵 {esc(track.get('title'))} <code>[{duration(track.get('duration'))}]</code>")
    if len(q) > 20:
        lines.append(f"\n…and {len(q)-20} more.")
    lines.append(f"\n<b>Total:</b> {len(q)} track(s)")
    return "\n".join(lines)
