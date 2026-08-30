import html
import time

STYLE = {
    "a": "ᴧ", "e": "є", "o": "σ", "n": "η", "u": "υ",
}
SMALLCAPS = {
    "a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ғ","g":"ɢ",
    "h":"ʜ","i":"ɪ","j":"ᴊ","k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ",
    "o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ","u":"ᴜ",
    "v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ",
}

def esc(value):
    return html.escape(str(value or ""))

def smallcaps(text):
    return "".join(
        STYLE.get(ch.lower(), SMALLCAPS.get(ch.lower(), ch)) if ch.isalpha() else ch
        for ch in str(text)
    )

def duration(seconds):
    try:
        seconds = int(seconds)
    except Exception:
        return "??:??"
    h, rem = divmod(max(0, seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def progress(current, total, width=12):
    if not total:
        return "━━━━━━━━━━━━"
    pos = max(0, min(width - 1, int((current / total) * width)))
    return "━" * pos + "●" + "━" * (width - pos - 1)

def uptime(start):
    sec = int(time.monotonic() - start)
    d, sec = divmod(sec, 86400)
    h, sec = divmod(sec, 3600)
    m, s = divmod(sec, 60)
    return f"{d}d {h}h {m}m {s}s" if d else f"{h}h {m}m {s}s"

def user_label(user):
    if not user:
        return "Unknown"
    name = " ".join(x for x in [user.first_name, user.last_name] if x)
    return esc(name or user.username or str(user.id))

def track_text(track, index=None):
    title = esc(track.get("title", "Unknown"))
    dur = duration(track.get("duration"))
    prefix = f"<b>{index}.</b> " if index is not None else ""
    return f"{prefix}<b>{title}</b> <code>[{dur}]</code>"
