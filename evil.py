# evil.py
# Enhanced Evil Discord Bot with reply chance control and VIP trolling

import os
import asyncio
import random
import logging
from threading import Thread

import discord
from flask import Flask
from dotenv import load_dotenv

from openrouter import get_smart_reply


# ==================================================
# Environment
# ==================================================

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "DISCORD_BOT_TOKEN is missing. Add it in Render Environment."
    )


# ==================================================
# Logging
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)

logger = logging.getLogger("evil-bot")


# ==================================================
# Flask Keep-Alive Server
# ==================================================

app = Flask(__name__)


@app.route("/")
def home():
    return "Evil Bot is running!", 200


@app.route("/health")
def health():
    return {
        "status": "online",
        "bot": "Evil",
    }, 200


def run_flask():
    port = int(os.getenv("PORT", "8080"))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False,
    )


# Start Flask in background
flask_thread = Thread(
    target=run_flask,
    daemon=True,
)

flask_thread.start()


# ==================================================
# Discord Setup
# ==================================================

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)


# ==================================================
# Evil Bot Variables
# ==================================================

evil_mode = True
reply_chance = 0.3

vip_users = set()
vip_trolling_enabled = True

nickname_task = None


# ==================================================
# Evil Nicknames
# ==================================================

evil_names = [
    "Little Devil 😈",
    "Tnyu",
    "Cursed Soul 👹",
    "Nightmare Fuel ☠️",
    "Dark Bean 🫘",
    "Tiny Terror 🧨",
    "Ghoulie 💀",
    "Meow of Doom 🐱‍👤",
    "Sinister Smile 😏",
    "Corrupted Angel 👿",
    "Sir Slaps-a-lot 🖐️",
    "Glitched Out 🤯",
    "Mister Mischief 🧛",
    "Bad Boi 🔥",
    "Sheesh Master 🥵",
    "Hell Baby 😇🔥",
    "Toxic AF ☣️",
    "Booty Whisperer 🍑🕵️‍♂️",
    "Spicy Pickle 🥒🔥",
    "Drama Daddy 🎭👊",
    "Simp Slayer 💔🔪",
    "Whip It Good 🔗😈",
    "Queen of Chaos 👑🧨",
    "Sugar Wreck 🍭💥",
    "Smooth Criminal 🎩🕶️",
    "Lurking Legend 👀⚔️",
    "Midnight Snack 🌙😋",
    "Twerkzilla 🍑🦖",
    "Hard Drive 💾💥",
    "FlirtBot9000 🤖💋",
    "Sir Glitch-a-lot 🧠⚡",
    "Chaos Magnet 🧲💢",
    "Savage Mode 🔥😤",
    "UwU Killer 🥺🔫",
    "Slap Happy ✋🤣",
    "Meme Reaper 💀😂",
    "Fake Innocent 😇😏",
    "No Filter 😶‍🌫️📢",
    "Mr. Smooth 🎩😌",
    "Sussy Legend 😳🏆",
    "Heartbreaker 2.0 💔💾",
    "Queen of Sass 👑😤",
    "Snacc Attack 🍬💣",
    "Emoji Dealer 😂💊",
    "Sly Fox 🦊😉",
    "Tongue Twister 👅🌀",
    "Zero Chill ❄️🔥",
    "Cringe King 😬👑",
    "Sinister Cutie 😈🥰",
    "Pixel Demon 💻👿",
    "Cloud Chaser ☁️💨",
    "Fake Lover 💘🕵️",
    "Spill Queen 🫖👑",
    "Late Night Vibes 🌙✨",
    "Bad Decision 🎲😏",
    "Mood Swinger 😵💫",
    "Laugh Assassin 😂🔪",
    "Caffeine Chaos ☕💥",
    "Red Flag 🚩💘",
    "Plot Twister 🔄📖",
    "Unstable Genius 🧠💣",
    "Drama Dealer 🎭🧨",
    "Silent Scream 😶🔊",
    "Heartbreak Hacker 💔💻",
    "Emo Energy 🖤🔋",
    "Mood Machine 😠➡️😜",
    "Sweet Chaos 🍭🧨",
    "Sleepy Evil 😴😈",
    "Innocent Devil 😇😈",
    "Soft Villain 🧸👿",
    "Dark Mode Activated 🌑💻",
    "Fictional Threat 📚⚠️",
    "Fluffy Menace 🐇💢",
    "Cool Disaster 🧊💥",
    "Cheeky Phantom 👻😏",
    "Casual Rogue 🧥🎯",
    "Trouble Vibes 🔊🚫",
    "Wholesome Bait 🎣🥺",
    "Toxic Tickle ☠️😂",
    "Laugh n’ Roast 🔥🤣",
    "Secret Sauce 🥫😜",
    "Zoned Out 🌀💤",
    "Simp Scanner 🔍💘",
    "Spicy Energy 🌶️⚡",
    "Whiplash Mood 🎢😎",
    "Overthink Tank 🧠💭",
    "Not a Bot 🤖😏",
    "Moody Cutie 😠😍",
    "Passive Threat 🤐💣",
    "Chill Chaos ❄️🔊",
    "Offline Troll 📴👿",
    "Vibe Sniper 🎯🎶",
    "Lowkey Savage 🕶️😈",
    "Witty Phantom 👻🧠",
    "Plot Bunny 🐰🧠",
    "Alt Account 🎭👀",
    "Sarcasm.exe 💻🙃",
    "Smirking Soul 😏👻",
    "Blink Twice Bot 😵👀",
    "Shy But Psycho 🫣🔪",
    "Clapback Kid 👏😤",
    "IYKYK 😌🤫",
    "Touch Grass 🌱😠",
    "Vibe Pirate 🏴‍☠️🎶",
    "Drama Looper 🔁🎭",
]


# ==================================================
# Helpers
# ==================================================

def guess_gender(username):
    """
    Kept for compatibility with your old code.
    Currently not used to change the reply.
    """

    name = username.lower()

    if any(
        word in name
        for word in ["queen", "girl", "lady", "princess", "💖", "👑"]
    ):
        return "female"

    if any(
        word in name
        for word in ["king", "boy", "dude", "bro", "🔥", "😎"]
    ):
        return "male"

    return "neutral"


def style_reply(reply, gender="neutral"):
    """
    Safely style the AI response.
    """

    if not reply:
        return "Mera evil brain crash ho gaya. 😈"

    reply = str(reply).strip()

    if not reply:
        return "Mera evil brain crash ho gaya. 😈"

    # Keep response reasonably short for Discord
    if len(reply) > 500:
        reply = reply[:497].rstrip() + "..."

    if not reply.endswith("😈"):
        reply = f"{reply} 😈"

    return reply


# ==================================================
# Nickname Changer
# ==================================================

async def evil_nickname_changer():
    await client.wait_until_ready()

    while not client.is_closed():
        try:
            for guild in client.guilds:

                if not guild.me:
                    continue

                # Only members the bot can manage
                manageable_members = [
                    member
                    for member in guild.members
                    if (
                        not member.bot
                        and member != guild.me
                        and member.top_role < guild.me.top_role
                    )
                ]

                if not manageable_members:
                    continue

                target = random.choice(manageable_members)
                new_name = random.choice(evil_names)

                try:
                    old_name = target.display_name

                    await target.edit(
                        nick=new_name,
                        reason="Evil bot nickname trolling",
                    )

                    logger.info(
                        "Changed nickname of %s to %s",
                        old_name,
                        new_name,
                    )

                except discord.Forbidden:
                    logger.warning(
                        "No permission to change nickname in %s",
                        guild.name,
                    )

                except discord.HTTPException as error:
                    logger.warning(
                        "Nickname change failed: %s",
                        error,
                    )

            await asyncio.sleep(random.randint(300, 600))

        except asyncio.CancelledError:
            logger.info("Nickname changer task stopped.")
            break

        except Exception:
            logger.exception("Nickname change error")
            await asyncio.sleep(60)


# ==================================================
# Discord Events
# ==================================================

@client.event
async def on_ready():
    global nickname_task

    logger.info("Evil is online as %s", client.user)

    # Prevent duplicate nickname tasks after reconnect
    if nickname_task is None or nickname_task.done():
        nickname_task = asyncio.create_task(
            evil_nickname_changer()
        )


@client.event
async def on_message(message):
    global evil_mode
    global reply_chance
    global vip_users
    global vip_trolling_enabled

    try:
        # Ignore bot messages
        if message.author.bot:
            return

        content = message.content.strip()

        if not content:
            return

        content_lower = content.lower()
        username = message.author.display_name

        # ==================================================
        # Evil Commands
        # ==================================================

        if content_lower.startswith("!evil"):

            # !evil off
            if content_lower == "!evil off":
                evil_mode = False

                await message.channel.send(
                    "😇 Evil mode deactivated."
                )

                return

            # !evil on
            if content_lower == "!evil on":
                evil_mode = True

                await message.channel.send(
                    "😈 Evil mode activated!"
                )

                return

            # !evil chance 0.3
            if content_lower.startswith("!evil chance"):

                try:
                    parts = content.split()

                    if len(parts) < 3:
                        raise ValueError

                    new_chance = float(parts[2])

                    if 0 <= new_chance <= 1:
                        reply_chance = new_chance

                        await message.channel.send(
                            f"✨ Reply chance set to "
                            f"{reply_chance * 100:.0f}%"
                        )
                    else:
                        await message.channel.send(
                            "⚠️ Enter a number between 0 and 1."
                        )

                except ValueError:
                    await message.channel.send(
                        "⚠️ Use like `!evil chance 0.3`"
                    )

                return

            # !evil vip start
            if content_lower.startswith("!evil vip start"):
                vip_trolling_enabled = True

                await message.channel.send(
                    "😈 VIP trolling activated!"
                )

                return

            # !evil vip stop
            if content_lower.startswith("!evil vip stop"):
                vip_trolling_enabled = False

                await message.channel.send(
                    "😇 VIP trolling paused."
                )

                return

            # !evil vip add username
            if content_lower.startswith("!evil vip add"):

                parts = content.split(maxsplit=3)

                if len(parts) < 4:
                    await message.channel.send(
                        "⚠️ Use like `!evil vip add username`"
                    )
                    return

                name = parts[3].lower()
                vip_users.add(name)

                await message.channel.send(
                    f"👑 VIP **{name}** added!"
                )

                return

            # !evil vip remove username
            if content_lower.startswith("!evil vip remove"):

                parts = content.split(maxsplit=3)

                if len(parts) < 4:
                    await message.channel.send(
                        "⚠️ Use like `!evil vip remove username`"
                    )
                    return

                name = parts[3].lower()
                vip_users.discard(name)

                await message.channel.send(
                    f"❌ VIP **{name}** removed."
                )

                return

        # ==================================================
        # Evil Reply Logic
        # ==================================================

        if not evil_mode:
            return

        mentioned = client.user in message.mentions

        random_chance = random.random() < reply_chance

        is_vip = (
            message.author.name.lower()
            in vip_users
        )

        should_reply = (
            mentioned
            or random_chance
            or (
                vip_trolling_enabled
                and is_vip
            )
        )

        if not should_reply:
            return

        # Remove bot mention before sending to AI
        ai_content = content

        if client.user:
            ai_content = ai_content.replace(
                f"<@{client.user.id}>",
                "",
            )

            ai_content = ai_content.replace(
                f"<@!{client.user.id}>",
                "",
            )

        ai_content = ai_content.strip()

        if not ai_content:
            ai_content = "Hello Evil"

        logger.info(
            "Message from %s: %s",
            username,
            ai_content[:200],
        )

        # Correct typing indicator usage
        async with message.channel.typing():
            raw_reply = await get_smart_reply(ai_content)

        gender = guess_gender(username)
        final_reply = style_reply(raw_reply, gender)

        await message.channel.send(
            final_reply[:1900]
        )

    except discord.Forbidden:
        logger.error(
            "Discord permission error."
        )

    except discord.HTTPException as error:
        logger.error(
            "Discord HTTP error: %s",
            error,
        )

    except Exception:
        logger.exception(
            "Error in on_message"
        )


# ==================================================
# Start Bot
# ==================================================

try:
    client.run(TOKEN)

except Exception:
    logger.exception(
        "Error running the bot"
    )
