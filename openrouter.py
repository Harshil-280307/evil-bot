# openrouter.py (Updated for very short evil Hinglish replies)
import aiohttp
import os
import logging

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-7b-instruct"

async def get_smart_reply(user_message):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You're an evil, toxic villain who replies in short Hinglish (Gujarati-English mix). "
                        "Never explain. Replies must be only 1 line, very short, sarcastic, and cruel."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"].strip()
                else:
                    logging.error(f"OpenRouter API error {response.status}")
                    return "⚠️ Brain fried."
    except Exception as e:
        logging.exception("OpenRouter error")
        return "⚠️ My evil mind broke."
