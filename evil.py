# evil-bot.py (Enhanced with reply chance control and VIP trolling)
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

# Flask keep-alive
app = Flask('')
@app.route('/')
def home():
    return "Evil Bot is running!"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

# Logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

# Discord setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)

# Environment
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Evil bot variables
evil_mode = True
reply_chance = 0.3  # Default 30% chance to reply
vip_users = set()
vip_trolling_enabled = True

# Evil nicknames
evil_names = [
    "Little Devil 😈","Tnyu", "Cursed Soul 👹", "Nightmare Fuel ☠️", "Dark Bean 🫘",
    "Tiny Terror 🧨", "Ghoulie 💀", "Meow of Doom 🐱‍👤", "Sinister Smile 😏",
    "Corrupted Angel 👿", "Sir Slaps-a-lot 🖐️", "Glitched Out 🤯", "Mister Mischief 🧛",
    "Bad Boi 🔥", "Sheesh Master 🥵", "Hell Baby 😇🔥", "Toxic AF ☣️", "Booty Whisperer 🍑🕵️‍♂️",
    "Spicy Pickle 🥒🔥", "Drama Daddy 🎭👊", "Simp Slayer 💔🔪", "Whip It Good 🔗😈",
    "Queen of Chaos 👑🧨", "Sugar Wreck 🍭💥", "Smooth Criminal 🎩🕶️", "Lurking Legend 👀⚔️",
    "Midnight Snack 🌙😋", "Twerkzilla 🍑🦖", "Hard Drive 💾💥", "FlirtBot9000 🤖💋",
    "Sir Glitch-a-lot 🧠⚡", "Chaos Magnet 🧲💢", "Savage Mode 🔥😤", "UwU Killer 🥺🔫",
    "Slap Happy ✋🤣", "Meme Reaper 💀😂", "Fake Innocent 😇😏", "No Filter 😶‍🌫️📢",
    "Mr. Smooth 🎩😌", "Sussy Legend 😳🏆", "Heartbreaker 2.0 💔💾", "Queen of Sass 👑😤",
    "Snacc Attack 🍬💣", "Emoji Dealer 😂💊", "Sly Fox 🦊😉", "Tongue Twister 👅🌀",
    "Zero Chill ❄️🔥", "Cringe King 😬👑", "Sinister Cutie 😈🥰", "Pixel Demon 💻👿",
    "Cloud Chaser ☁️💨", "Fake Lover 💘🕵️", "Spill Queen 🫖👑", "Late Night Vibes 🌙✨",
    "Bad Decision 🎲😏", "Mood Swinger 😵💫", "Laugh Assassin 😂🔪", "Caffeine Chaos ☕💥",
    "Red Flag 🚩💘", "Plot Twister 🔄📖", "Unstable Genius 🧠💣", "Drama Dealer 🎭🧨",
    "Silent Scream 😶🔊", "Heartbreak Hacker 💔💻", "Emo Energy 🖤🔋", "Mood Machine 😠➡️😜",
    "Sweet Chaos 🍭🧨", "Sleepy Evil 😴😈", "Innocent Devil 😇😈", "Soft Villain 🧸👿",
    "Dark Mode Activated 🌑💻", "Fictional Threat 📚⚠️", "Fluffy Menace 🐇💢",
    "Cool Disaster 🧊💥", "Cheeky Phantom 👻😏", "Casual Rogue 🧥🎯", "Trouble Vibes 🔊🚫",
    "Wholesome Bait 🎣🥺", "Toxic Tickle ☠️😂", "Laugh n’ Roast 🔥🤣", "Secret Sauce 🥫😜",
    "Zoned Out 🌀💤", "Simp Scanner 🔍💘", "Spicy Energy 🌶️⚡", "Whiplash Mood 🎢😎",
    "Overthink Tank 🧠💭", "Not a Bot 🤖😏", "Moody Cutie 😠😍", "Passive Threat 🤐💣",
    "Chill Chaos ❄️🔊", "Offline Troll 📴👿", "Vibe Sniper 🎯🎶", "Lowkey Savage 🕶️😈",
    "Witty Phantom 👻🧠", "Plot Bunny 🐰🧠", "Alt Account 🎭👀", "Sarcasm.exe 💻🙃",
    "Smirking Soul 😏👻", "Blink Twice Bot 😵👀", "Shy But Psycho 🫣🔪", "Clapback Kid 👏😤",
    "IYKYK 😌🤫", "Touch Grass 🌱😠", "Vibe Pirate 🏴‍☠️🎶", "Drama Looper 🔁🎭"
]


def guess_gender(username):
    name = username.lower()
    if any(word in name for word in ['queen', 'girl', 'lady', 'princess', '💖', '👑']):
        return 'female'
    elif any(word in name for word in ['king', 'boy', 'dude', 'bro', '🔥', '😎']):
        return 'male'
    return 'neutral'

def style_reply(reply, gender):
    return f"{reply.strip().split('.')[0][:80]} 😈"

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
                        pass
            await asyncio.sleep(random.randint(300, 600))
        except Exception as e:
            logging.exception("Nickname change error")
            await asyncio.sleep(60)

@client.event
async def on_ready():
    logging.info(f"Evil is online as {client.user}")
    client.loop.create_task(evil_nickname_changer())

@client.event
async def on_message(message):
    global evil_mode, reply_chance, vip_users, vip_trolling_enabled

    try:
        if message.author.bot:
            return

        content = message.content.strip()
        content_lower = content.lower()
        username = message.author.display_name

        # Evil commands
        if content_lower.startswith("!evil"):
            if content_lower == "!evil off":
                evil_mode = False
                await message.channel.send("😇 Evil mode deactivated.")
                return
            elif content_lower == "!evil on":
                evil_mode = True
                await message.channel.send("😈 Evil mode activated!")
                return
            elif content_lower.startswith("!evil chance"):
                try:
                    new_chance = float(content.split()[2])
                    if 0 <= new_chance <= 1:
                        reply_chance = new_chance
                        await message.channel.send(f"✨ Reply chance set to {reply_chance * 100:.0f}%")
                    else:
                        await message.channel.send("⚠️ Enter a number between 0 and 1.")
                except:
                    await message.channel.send("⚠️ Use like `!evil chance 0.3`")
                return
            elif content_lower.startswith("!evil vip start"):
                vip_trolling_enabled = True
                await message.channel.send("😈 VIP trolling activated!")
                return
            elif content_lower.startswith("!evil vip stop"):
                vip_trolling_enabled = False
                await message.channel.send("😇 VIP trolling paused.")
                return
            elif content_lower.startswith("!evil vip add"):
                try:
                    name = content.split()[3].lower()
                    vip_users.add(name)
                    await message.channel.send(f"👑 VIP **{name}** added!")
                except:
                    await message.channel.send("⚠️ Use like `!evil vip add username`")
                return
            elif content_lower.startswith("!evil vip remove"):
                try:
                    name = content.split()[3].lower()
                    vip_users.discard(name)
                    await message.channel.send(f"❌ VIP **{name}** removed.")
                except:
                    await message.channel.send("⚠️ Use like `!evil vip remove username`")
                return

        if not evil_mode:
            return

        mentioned = client.user in message.mentions
        random_chance = random.random() < reply_chance
        is_vip = message.author.name.lower() in vip_users

        if mentioned or random_chance or (vip_trolling_enabled and is_vip):
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
