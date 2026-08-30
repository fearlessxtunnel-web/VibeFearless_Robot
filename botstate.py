_enabled = True

def is_enabled():
    return _enabled

def set_enabled(value):
    global _enabled
    _enabled = bool(value)
