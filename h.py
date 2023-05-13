from pyrogram import Client

api_id = 
api_hash = ""
bot_token = ""

app = Client(
    "my_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)

app.run()
