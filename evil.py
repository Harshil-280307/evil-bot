# evil.py
import discord
import asyncio
from flask import Flask
from threading import Thread
from openrouter import get_smart_reply
import logging
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

# Flask server to keep alive
app = Flask('')

@app.route('/')
def home():
    return "Evil Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

flask_thread = Thread(target=run_flask)
flask_thread.start()

# Discord setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Gender guesser
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

@client.event
async def on_ready():
    logging.info(f"Evil is online as {client.user}")

@client.event
async def on_message(message):
    try:
        if message.author.bot:
            return
        content = message.content
        username = message.author.display_name

        if client.user.mentioned_in(message) or message.channel.type.name == "private" or "evil" in content.lower():
            await message.channel.typing()
            raw_reply = await get_smart_reply(content)
            gender = guess_gender(username)
            final_reply = style_reply(raw_reply, gender)
            await message.channel.send(final_reply)

    except Exception as e:
        logging.exception("Error in on_message")

try:
    client.run(TOKEN)
except Exception as e:
    logging.exception("Error running the bot")
