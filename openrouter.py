
# openrouter.py
# OpenRouter AI backend for Evil Discord Bot

import aiohttp
import asyncio
import os
import logging


# =========================================================
# OPENROUTER CONFIGURATION
# =========================================================

API_KEY = os.getenv("OPENROUTER_API_KEY")

# OpenRouter's free model router.
# It automatically selects an available free model.
MODEL = "openrouter/free"

API_URL = "https://openrouter.ai/api/v1/chat/completions"


# =========================================================
# GET AI REPLY
# =========================================================

async def get_smart_reply(user_message):

    try:

        # -------------------------------------------------
        # Check API key
        # -------------------------------------------------

        if not API_KEY:
            logging.error(
                "OPENROUTER_API_KEY is missing from environment variables."
            )
            return "⚠️ OpenRouter key missing."


        # -------------------------------------------------
        # Headers
        # -------------------------------------------------

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",

            # OpenRouter metadata
            "HTTP-Referer": "https://evil-bot-mvpp.onrender.com",
            "X-Title": "Evil Discord Bot"
        }


        # -------------------------------------------------
        # Request payload
        # -------------------------------------------------

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
                    "content": user_message
                }
            ],

            # Keep replies short
            "max_tokens": 80,

            # Give the bot some personality
            "temperature": 0.9
        }


        # -------------------------------------------------
        # HTTP TIMEOUT
        # -------------------------------------------------

        timeout = aiohttp.ClientTimeout(total=30)


        # -------------------------------------------------
        # SEND REQUEST TO OPENROUTER
        # -------------------------------------------------

        async with aiohttp.ClientSession(
            timeout=timeout
        ) as session:

            async with session.post(
                API_URL,
                headers=headers,
                json=payload
            ) as response:


                # -----------------------------------------
                # READ RESPONSE
                # -----------------------------------------

                try:
                    data = await response.json()

                except Exception:

                    text = await response.text()

                    logging.error(
                        "OpenRouter returned invalid JSON: "
                        f"{text}"
                    )

                    return "⚠️ Evil brain got corrupted."


                # -----------------------------------------
                # SUCCESS
                # -----------------------------------------

                if response.status == 200:

                    try:

                        reply = data["choices"][0]["message"]["content"]

                        reply = reply.strip()

                        if not reply:

                            logging.error(
                                "OpenRouter returned an empty reply."
                            )

                            return (
                                "⚠️ Evil brain is speechless."
                            )

                        logging.info(
                            "OpenRouter response received successfully."
                        )

                        return reply


                    except (
                        KeyError,
                        IndexError,
                        TypeError
                    ):

                        logging.error(
                            "Unexpected OpenRouter response format: "
                            f"{data}"
                        )

                        return (
                            "⚠️ Evil brain got confused."
                        )


                # -----------------------------------------
                # ERROR LOGGING
                # -----------------------------------------

                logging.error(
                    f"OpenRouter API error {response.status}: {data}"
                )


                # -----------------------------------------
                # 401 - INVALID API KEY
                # -----------------------------------------

                if response.status == 401:

                    logging.error(
                        "OpenRouter API key is invalid or missing."
                    )

                    return "⚠️ Evil key rejected."


                # -----------------------------------------
                # 402 - PAYMENT / CREDITS
                # -----------------------------------------

                elif response.status == 402:

                    logging.error(
                        "OpenRouter account has a credits/payment issue."
                    )

                    return "⚠️ Evil wallet is empty."


                # -----------------------------------------
                # 404 - MODEL / ENDPOINT
                # -----------------------------------------

                elif response.status == 404:

                    logging.error(
                        "OpenRouter could not find the requested "
                        f"resource. MODEL={MODEL}"
                    )

                    return "⚠️ Evil AI disappeared."


                # -----------------------------------------
                # 429 - RATE LIMIT
                # -----------------------------------------

                elif response.status == 429:

                    logging.error(
                        "OpenRouter rate limit or free-tier limit reached."
                    )

                    return (
                        "⚠️ Too many victims. Try again later."
                    )


                # -----------------------------------------
                # OTHER ERRORS
                # -----------------------------------------

                return "⚠️ Evil AI is temporarily broken."


    # =====================================================
    # TIMEOUT ERROR
    # =====================================================

    except asyncio.TimeoutError:

        logging.error(
            "OpenRouter request timed out."
        )

        return "⚠️ Evil brain is taking a nap."


    # =====================================================
    # GENERAL ERROR
    # =====================================================

    except Exception:

        logging.exception(
            "OpenRouter error"
        )

        return "⚠️ My evil mind broke."
