import asyncio
import re
from urllib.parse import urlparse

import yt_dlp

import config

URL_RE = re.compile(r"^https?://", re.I)

def is_url(text):
    return bool(URL_RE.match(text.strip()))

def _search_sync(query):
    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": True,
        "noplaylist": True,
        "default_search": "ytsearch1",
        "socket_timeout": config.SEARCH_TIMEOUT,
    }
    target = query if is_url(query) else f"ytsearch1:{query}"
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(target, download=False)
        if not info:
            return None
        if "entries" in info:
            info = next((x for x in info["entries"] if x), None)
        if not info:
            return None
        webpage = info.get("webpage_url") or info.get("original_url") or info.get("url")
        return {
            "id": info.get("id"),
            "title": info.get("title") or "Unknown title",
            "duration": info.get("duration") or 0,
            "thumbnail": info.get("thumbnail"),
            "webpage_url": webpage,
            "uploader": info.get("uploader") or "Unknown",
        }

async def search(query):
    return await asyncio.wait_for(
        asyncio.to_thread(_search_sync, query),
        timeout=config.SEARCH_TIMEOUT + 5,
    )

def _stream_sync(webpage_url):
    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "format": "bestaudio/best",
        "noplaylist": True,
        "socket_timeout": config.STREAM_TIMEOUT,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(webpage_url, download=False)
        if not info:
            raise RuntimeError("No media information returned")
        if info.get("entries"):
            info = next((x for x in info["entries"] if x), None)
        url = info.get("url")
        if not url:
            raise RuntimeError("No direct audio stream found")
        return url, info.get("duration") or 0, info.get("title") or "Unknown title"

async def get_stream(webpage_url):
    return await asyncio.wait_for(
        asyncio.to_thread(_stream_sync, webpage_url),
        timeout=config.STREAM_TIMEOUT + 10,
    )
