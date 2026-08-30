# ⚡ VIBE FEARLESS

Telegram voice-chat music bot with a fast UI, queue, inline player controls and a dedicated **FEARLESS ASSISTANT** account.

**Owned by:** @Fearless45op  
**Channel:** @SPARK_X_NETWORK_OP  
**Group:** @SPARK_X_NETWORK

## Features

- `/play <song>` search and voice-chat playback
- Queue with limits
- Auto next when a stream ends
- Pause / resume / skip / stop
- Shuffle
- Loop current track
- Per-chat volume 1–200
- Inline player buttons
- Queue and Now Playing UI
- Owner ON/OFF switch
- MongoDB support with graceful no-Mongo fallback
- Render health endpoint
- Keep-alive support
- Assistant auto-join attempts
- Dedicated assistant session
- Automatic restart loop on transient process errors

## Important

A Telegram bot token alone cannot act as the voice-chat participant. The project uses a dedicated Telegram user account as **FEARLESS ASSISTANT** for PyTgCalls. Add that account to the target group and give it the permissions needed for your group.

Do not use your personal account for the assistant session.

## Setup

1. Create a bot with `@BotFather`.
2. Get `API_ID` and `API_HASH` from Telegram.
3. Create a dedicated Telegram account for the assistant.
4. Run:

```bash
python3 generate_session.py
```

5. Copy the generated `STRING_SESSION`.
6. Copy `.env.example` to `.env` and fill in the values.
7. Install:

```bash
pip install -r requirements.txt
```

8. Make sure FFmpeg is installed.
9. Start:

```bash
python3 app.py
```

## Group usage

Add the bot and the FEARLESS ASSISTANT account to your group.

Then:

```text
/play Believer
```

The assistant joins the active voice chat and playback starts.

## Notes

No software can honestly guarantee zero errors: Telegram, YouTube/source availability, network conditions, API changes and hosting limits can fail outside the application's control. This build uses current PyTgCalls 2.x-style APIs and defensive error handling to reduce common failures.

## Integrated remaining modules

This package now includes the richer uploaded `play.py`, `nowplaying.py`,
`progress.py`, and `youtube.py` modules, including live progress updates,
inline seek controls, replay, autoplay, start-media management and broadcast
handlers.

### Security

Never publish `.env`, API keys, bot tokens, assistant sessions, or database
connection strings. If a real MongoDB URI or API key has ever been exposed,
rotate/revoke it before deploying this package.
