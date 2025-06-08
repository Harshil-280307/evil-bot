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
from deep_translator import GoogleTranslator

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

# Gujarati + English evil-style enhancer
def evilify_reply(reply, original):
    guj_phrases = [
        "તને શરમ નથી આવતી? 😈",
        "તારું દિમાગ ફ્રાઈ છે કે શું? 🤡",
        "મને જોઈને ડરી ગયો ને? 👹",
        "તું તો ભૂલનાર મજૂર છે. 💀",
        "હવે તું મારી લિસ્ટમાં છે. 🧿",
        "હસ્યા વગર ડરાવું છું હું. 😏",
        "તમારું અસ્તિત્વ તુચ્છ છે. 🔥"
    ]
    eng_phrases = [
        "You're nothing but a pawn. ☠️",
        "Bow before me, mortal. 😈",
        "Your words are weak. 💀",
        "I feast on your failures. 👿",
        "Kneel, insect. 🔥",
        "I'm always watching... 🧿",
        "Suffer in silence. 🕷️"
    ]

    if any(char in original for char in "અઆઇઈઉઊએઐઓઔકખગઘચછજઝટઠડઢતથદધનપફબભમયરલવશષસહળંઁઽ"):
        return f"{reply} — {random.choice(guj_phrases)}"
    else:
        return f"{reply} — {random.choice(eng_phrases)}"

def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text

@client.event
async def on_ready():
    logging.info(f"Evil is online as {client.user}")

@client.event
async def on_message(message):
    try:
        if message.author.bot:
            return

        content = message.content.strip()

        if random.random() < 0.2:
            await asyncio.sleep(1)
            await message.delete()
            await message.channel.send(f"{message.author.mention}, your message was too weak to exist. ☠️")
            return

        await message.channel.typing()

        translated = translate_to_english(content)
        raw_reply = await get_smart_reply(translated)
        evil_reply = evilify_reply(raw_reply, content)
        await message.channel.send(evil_reply)

        if random.random() < 0.3:
            await message.add_reaction("😈")

        if random.random() < 0.1:
            try:
                evil_names = ["ભયાનક", "વિનાશક", "જરૂરી ગુલામ", "હારી ગયેલો", "ફિલ્મી ખલનાયક"]
                new_nick = random.choice(evil_names)
                await message.author.edit(nick=new_nick)
                await message.channel.send(f"{message.author.mention}, હવે તારું નામ '{new_nick}' છે. મજા આવી ગઈ? 👹")
            except:
                pass

    except Exception as e:
        logging.exception("Error in on_message")

try:
    client.run(TOKEN)
except Exception as e:
    logging.exception("Error running the bot")
