# evil.py
import discord
import asyncio
from flask import Flask
from threading import Thread
from openrouter import get_smart_reply
import logging
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

# Keep Alive Flask Server
app = Flask('')

@app.route('/')
def home():
    return "Evil Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_flask).start()

# Discord Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Gender Style Helpers
def guess_gender(username):
    name = username.lower()
    if any(word in name for word in ['queen', 'girl', 'lady', 'princess', '💖', '👑']):
        return 'female'
    elif any(word in name for word in ['king', 'boy', 'dude', 'bro', '🔥', '😎']):
        return 'male'
    else:
        return 'neutral'

def style_reply(reply, gender):
    if gender == 'female':
        return f"{reply} 💖✨"
    elif gender == 'male':
        return f"{reply} 😎🔥"
    else:
        return f"{reply} 🤖"

# On Ready
@client.event
async def on_ready():
    logging.info(f"Evil is online as {client.user}")

# On Message
@client.event
async def on_message(message):
    try:
        if message.author.bot:
            return
        content = message.content
        username = message.author.display_name

        if client.user.mentioned_in(message) or "evil" in content.lower():
            await message.channel.typing()
            raw_reply = await get_smart_reply(content)
            logging.info(f"Reply: {raw_reply}")
            gender = guess_gender(username)
            final_reply = style_reply(raw_reply, gender)
            await message.channel.send(final_reply)

    except Exception as e:
        logging.exception("Error in on_message")

try:
    client.run(TOKEN)
except Exception as e:
    logging.exception("Error running the bot")
