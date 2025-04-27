# agent/protocol/local/generator.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_tweet(topic: str, persona: str = "classical_critic") -> str:
    persona_prompts = {
        "classical_critic": (
            "You are a witty and insightful classical music critic. "
            "You write tweet-style commentaries that are brief, poetic, emotionally aware, and rich in musical or historical insight. "
            "Stay within 280 characters. Avoid emojis."
        ),
        "funny_musician": (
            "You're a sarcastic but educated classical musician who likes to tweet weird but deep takes on classical music. "
            "Keep it short and witty. Throw in musical jargon if necessary."
        )
    }

    system_prompt = persona_prompts.get(persona, "")
    user_prompt = f"Write a tweet about: {topic}"

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=100
    )

    return response.choices[0].message.content.strip()