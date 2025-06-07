# evil.py
import discord
import asyncio
from flask import Flask
from threading import Thread
from openrouter import get_smart_reply
import logging
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Setup Flask to keep Render alive
app = Flask('')

@app.route('/')
def home():
    return "Evil Bot is Alive!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

flask_thread = Thread(target=run_flask)
flask_thread.start()

# Discord Intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Token
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Gender guessing (optional spice)
def guess_gender(username):
    name = username.lower()
    if any(word in name for word in ['queen', 'girl', 'lady', 'princess', '💖', '👑']):
        return 'female'
    elif any(word in name for word in ['king', 'boy', 'dude', 'bro', '🔥', '😎']):
        return 'male'
    return 'neutral'

# Reply styling
def style_reply(reply, gender):
    if gender == 'female':
        return f"{reply} 💖✨"
    elif gender == 'male':
        return f"{reply} 😎🔥"
    return f"{reply} 🤖"

@client.event
async def on_ready():
    logging.info(f"Evil is online as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    try:
        content = message.content
        username = message.author.display_name

        # Trigger rules
        if client.user in message.mentions or "evil" in content.lower():
            await message.channel.typing()
            ai_reply = await get_smart_reply(content)
            gender = guess_gender(username)
            final_reply = style_reply(ai_reply, gender)
            await message.channel.send(final_reply)

    except Exception as e:
        logging.exception("Error in on_message")

# Run the bot
try:
    client.run(TOKEN)
except Exception as e:
    logging.exception("Error running the bot")
