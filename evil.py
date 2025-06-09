import discord
import asyncio
import random
from flask import Flask
from threading import Thread
from openrouter import get_smart_reply
import logging
import os
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

evil_mode = True

evil_names = [
    "Little Devil 😈", "Cursed Soul 👹", "Nightmare Fuel ☠️", "Dark Bean 🫘",
    "Tiny Terror 🧨", "Ghoulie 💀", "Meow of Doom 🐱‍👤", "Sinister Smile 😏",
    "Corrupted Angel 👿", "Sir Slaps-a-lot 🖐️", "Glitched Out 🤯", "Mister Mischief 🧛"
]

def guess_gender(username):
    name = username.lower()
    if any(word in name for word in ['queen', 'girl', 'lady', 'princess', '💖', '👑']):
        return 'female'
    elif any(word in name for word in ['king', 'boy', 'dude', 'bro', '🔥', '😎']):
        return 'male'
    else:
        return 'neutral'

def style_reply(reply, gender):
    short_reply = reply.strip().split('.')[0][:80]
    return f"{short_reply} 😈"

async def evil_nickname_changer():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            for guild in client.guilds:
                members = [m for m in guild.members if not m.bot and m.nick != client.user.name]
                if members:
                    target = random.choice(members)
                    new_name = random.choice(evil_names)
                    try:
                        await target.edit(nick=new_name)
                        logging.info(f"Changed nickname of {target.display_name} to {new_name}")
                    except:
                        pass  # Avoid errors if missing permissions
            await asyncio.sleep(random.randint(300, 600))  # every 5–10 mins
        except Exception as e:
            logging.exception("Nickname change error")
            await asyncio.sleep(60)

@client.event
async def on_ready():
    logging.info(f"Evil is online as {client.user}")
    client.loop.create_task(evil_nickname_changer())

@client.event
async def on_message(message):
    global evil_mode

    try:
        if message.author.bot:
            return

        content = message.content.strip()
        content_lower = content.lower()
        username = message.author.display_name

        # Toggle evil mode
        if content_lower.startswith("!evil"):
            if content_lower == "!evil off":
                evil_mode = False
                await message.channel.send("😇 Evil mode deactivated. I'm behaving now...")
                return
            elif content_lower == "!evil on":
                evil_mode = True
                await message.channel.send("😈 Evil mode activated! Let the torment begin!")
                return

        if not evil_mode:
            return

        # Evil change self
        if "evil change" in content_lower:
            new_nick = random.choice(evil_names)
            try:
                await message.author.edit(nick=new_nick)
                await message.channel.send(f"😈 Nickname cursed to **{new_nick}**!")
            except:
                await message.channel.send("🔒 I can't change your nickname! I need permission.")
            return

        # Change someone else using command
        if content_lower.startswith("!change \""):
            try:
                target_name = content.split('"')[1]
                found = False
                for member in message.guild.members:
                    if member.name.lower() == target_name.lower() and not member.bot:
                        new_nick = random.choice(evil_names)
                        try:
                            await member.edit(nick=new_nick)
                            await message.channel.send(f"😈 Renamed **{member.name}** to **{new_nick}**")
                        except:
                            await message.channel.send(f"🔒 Can't rename {member.name}. No permission.")
                        found = True
                        break
                if not found:
                    await message.channel.send(f"👀 No user named '{target_name}' found.")
            except:
                await message.channel.send("⚠️ Use the format: `!change \"username\"`")
            return

        # Evil reply
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
