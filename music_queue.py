import asyncio
import random
from collections import defaultdict

_queues = defaultdict(list)
_now_playing = {}
_states = defaultdict(lambda: "idle")
_volumes = defaultdict(lambda: 100)
_loops = defaultdict(lambda: False)
_autoplay = defaultdict(lambda: False)
_locks = defaultdict(asyncio.Lock)

def lock(chat_id):
    return _locks[chat_id]

def queue(chat_id):
    return _queues[chat_id]

def add(chat_id, track):
    _queues[chat_id].append(track)
    return len(_queues[chat_id])

def pop(chat_id):
    return _queues[chat_id].pop(0) if _queues[chat_id] else None

def clear_queue(chat_id):
    _queues[chat_id].clear()

def set_now(chat_id, track):
    if track is None:
        _now_playing.pop(chat_id, None)
        _states[chat_id] = "idle"
    else:
        _now_playing[chat_id] = track
        _states[chat_id] = "playing"

def now(chat_id):
    return _now_playing.get(chat_id)

def set_state(chat_id, state):
    _states[chat_id] = state

def state(chat_id):
    return _states[chat_id]

def set_volume(chat_id, value):
    _volumes[chat_id] = max(1, min(200, int(value)))
    return _volumes[chat_id]

def volume(chat_id):
    return _volumes[chat_id]

def toggle_loop(chat_id):
    _loops[chat_id] = not _loops[chat_id]
    return _loops[chat_id]

def loop(chat_id):
    return _loops[chat_id]

def toggle_autoplay(chat_id):
    _autoplay[chat_id] = not _autoplay[chat_id]
    return _autoplay[chat_id]

def autoplay(chat_id):
    return _autoplay[chat_id]

def shuffle(chat_id):
    random.shuffle(_queues[chat_id])

def clear(chat_id):
    _queues.pop(chat_id, None)
    _now_playing.pop(chat_id, None)
    _states.pop(chat_id, None)
    _volumes.pop(chat_id, None)
    _loops.pop(chat_id, None)
    _autoplay.pop(chat_id, None)


def is_playing(chat_id):
    return chat_id in _now_playing


def get_now_playing(chat_id):
    return _now_playing.get(chat_id)


def get_state(chat_id):
    return _states[chat_id]


def push(chat_id, track):
    _queues[chat_id].append(track)
    return len(_queues[chat_id])


def pop_next(chat_id):
    return _queues[chat_id].pop(0) if _queues[chat_id] else None


def set_now_playing(chat_id, track):
    set_now(chat_id, track)
