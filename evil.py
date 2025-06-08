# evil-bot.py
import discord
import asyncio
from flask import Flask
from threading import Thread
from openrouter import get_smart_reply
import logging
import os
import random
from dotenv import load_dotenv

load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

# Flask server to keep alive
app = Flask('')

@app.route('/')
def home():
    return "Evil Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_flask).start()

# Discord setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Evil state per channel
evil_channels = set()

# Evil-style response enhancer
def evilify_reply(reply):
    phrases = [
        "You're nothing but a pawn. ☠️",
        "Bow before me, mortal. 😈",
        "Your words are weak, unlike my wrath. 💀",
        "I feast on your failures. 👿",
        "Kneel, insect. 🔥",
        "I'm always watching... 🧿",
        "Suffer in silence, or I will make you. 🕷️",
        "તને ભય લાગ્યો છે? 😈",
        "તમારી વાતોમાં કોઈ ભાર નથી. 💀",
        "હું તને હંમેશા જુએ છું... 🧿",
        "તું ફસાયો છે, હવે કેમ જુઓ. 🔥"
    ]
    return random.choice(phrases)

@client.event
async def on_ready():
    logging.info(f"Evil is online as {client.user}")

@client.event
async def on_message(message):
    try:
        if message.author.bot:
            return

        content = message.content.strip().lower()
        channel_id = message.channel.id

        # Per-channel toggle commands
        if content == "!evil on":
            evil_channels.add(channel_id)
            await message.channel.send("😈 Evil mode activated in this channel.")
            return

        if content == "!evil off":
            evil_channels.discard(channel_id)
            await message.channel.send("😇 Evil mode deactivated in this channel.")
            return

        # If evil mode OFF in this channel, do nothing
        if channel_id not in evil_channels:
            return

        # Evil behavior: sometimes delete message
        if random.random() < 0.2:
            await asyncio.sleep(1)
            await message.delete()
            await message.channel.send(f"{message.author.mention}, your message was too weak to exist. ☠️")
            return

        await message.channel.typing()
        raw_reply = await get_smart_reply(message.content)
        evil_reply = evilify_reply(raw_reply)
        await message.channel.send(evil_reply)

        # Evil reaction emoji
        if random.random() < 0.3:
            await message.add_reaction("😈")

        # Evil nickname change sometimes
        if random.random() < 0.1:
            try:
                evil_names = ["Peasant", "Weakling", "Fool", "Minion", "Loser", "ભયાનક", "વિનાશક", "મૂર્ખ"]
                new_nick = random.choice(evil_names)
                await message.author.edit(nick=new_nick)
                await message.channel.send(f"{message.author.mention}, you are now known as '{new_nick}'. Deal with it. 🧛")
            except:
                pass

    except Exception as e:
        logging.exception("Error in on_message")

try:
    client.run(TOKEN)
except Exception as e:
    logging.exception("Error running the bot")
