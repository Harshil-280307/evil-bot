
# openrouter.py
# OpenRouter AI backend for Evil Discord Bot

import aiohttp
import asyncio
import os
import logging


# =========================================================
# LOGGING
# =========================================================

logger = logging.getLogger(__name__)


# =========================================================
# OPENROUTER CONFIGURATION
# =========================================================

MODEL = "openrouter/free"

API_URL = "https://openrouter.ai/api/v1/chat/completions"

REFERER = "https://evil-bot-mvpp.onrender.com"

BOT_NAME = "Evil Discord Bot"


# =========================================================
# GET AI REPLY
# =========================================================

async def get_smart_reply(user_message):

    # Read API key at request time
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:

        logger.error(
            "OPENROUTER_API_KEY is missing."
        )

        return "⚠️ Evil key missing."

    if not isinstance(user_message, str) or not user_message.strip():

        logger.warning(
            "Empty user message received."
        )

        return "⚠️ Evil heard nothing."

    headers = {

        "Authorization": f"Bearer {api_key}",

        "Content-Type": "application/json",

        "HTTP-Referer": REFERER,

        "X-Title": BOT_NAME

    }

    payload = {

        "model": MODEL,

        "messages": [

            {
                "role": "system",

                "content": (
                    "You are Evil, a sarcastic and mischievous "
                    "Discord villain bot. "

                    "Reply in very short Hinglish with a natural "
                    "mix of Hindi, Gujarati and English. "

                    "Keep every response to ONE short line. "

                    "Be funny, sarcastic and playful. "

                    "Do not explain anything. "

                    "Do not write paragraphs. "

                    "Do not mention these instructions."
                )

            },

            {
                "role": "user",

                "content": user_message.strip()
            }

        ],

        "max_tokens": 80,

        "temperature": 0.9

    }

    timeout = aiohttp.ClientTimeout(
        total=30
    )

    try:

        async with aiohttp.ClientSession(
            timeout=timeout
        ) as session:

            async with session.post(
                API_URL,
                headers=headers,
                json=payload
            ) as response:

                # Read response as text first
                # This makes debugging much easier
                raw_text = await response.text()

                logger.info(
                    "OpenRouter status=%s model=%s",
                    response.status,
                    MODEL
                )

                # -------------------------------------------------
                # NON-200 ERROR
                # -------------------------------------------------

                if response.status != 200:

                    logger.error(
                        "OpenRouter API error | status=%s | body=%s",
                        response.status,
                        raw_text
                    )

                    if response.status == 401:
                        return "⚠️ Evil key rejected."

                    elif response.status == 402:
                        return "⚠️ Evil wallet is empty."

                    elif response.status == 404:
                        return "⚠️ Evil AI disappeared."

                    elif response.status == 429:
                        return "⚠️ Too many victims. Try again later."

                    elif response.status >= 500:
                        return "⚠️ Evil provider is sleeping."

                    return "⚠️ Evil AI is temporarily broken."

                # -------------------------------------------------
                # PARSE JSON
                # -------------------------------------------------

                try:

                    data = await response.json(
                        content_type=None
                    )

                except Exception:

                    logger.error(
                        "OpenRouter returned invalid JSON | body=%s",
                        raw_text
                    )

                    return "⚠️ Evil brain returned nonsense."

                # -------------------------------------------------
                # CHECK API ERROR INSIDE RESPONSE
                # -------------------------------------------------

                if "error" in data:

                    logger.error(
                        "OpenRouter response contains error: %s",
                        data["error"]
                    )

                    return "⚠️ Evil AI returned an error."

                # -------------------------------------------------
                # EXTRACT REPLY
                # -------------------------------------------------

                try:

                    reply = data["choices"][0]["message"]["content"]

                except (KeyError, IndexError, TypeError):

                    logger.error(
                        "Unexpected OpenRouter response format: %s",
                        data
                    )

                    return "⚠️ Evil brain got confused."

                if not isinstance(reply, str):

                    logger.error(
                        "OpenRouter reply is not text: %r",
                        reply
                    )

                    return "⚠️ Evil brain is speechless."

                reply = reply.strip()

                if not reply:

                    logger.error(
                        "OpenRouter returned empty reply."
                    )

                    return "⚠️ Evil brain is speechless."

                logger.info(
                    "OpenRouter reply received successfully."
                )

                return reply

    # =====================================================
    # TIMEOUT ERROR
    # =====================================================

    except asyncio.TimeoutError:

        logger.exception(
            "OpenRouter request timed out."
        )

        return "⚠️ Evil brain is taking a nap."

    # =====================================================
    # HTTP CLIENT ERROR
    # =====================================================

    except aiohttp.ClientError:

        logger.exception(
            "OpenRouter HTTP client error."
        )

        return "⚠️ Evil cannot reach the AI."

    # =====================================================
    # GENERAL ERROR
    # =====================================================

    except Exception:

        logger.exception(
            "Unexpected OpenRouter error."
        )

        return "⚠️ My evil mind broke."
