from pyrogram import Client

print("Generate a STRING_SESSION for the dedicated FEARLESS ASSISTANT account.")
api_id = int(input("API_ID: ").strip())
api_hash = input("API_HASH: ").strip()

with Client(
    "fearless_assistant_session",
    api_id=api_id,
    api_hash=api_hash,
    in_memory=True,
) as app:
    print("\nSTRING_SESSION:\n")
    print(app.export_session_string())
    print("\nKeep this secret. Never publish it.")
