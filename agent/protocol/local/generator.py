# agent/protocol/local/generator.py

import os
from openai import AsyncOpenAI
from agent.model.persona import PersonaManager

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
persona_manager = PersonaManager()

async def generate_tweet(topic: str, persona: str = "classical_critic") -> dict:
    """Generate a tweet about a given topic using the specified persona."""
    # Get the persona configuration
    persona_obj = persona_manager.get_persona(persona)
    if not persona_obj:
        raise ValueError(f"Persona '{persona}' not found")
    
    # Get the system prompt from the persona
    system_prompt = persona_obj.get_system_prompt()
    user_prompt = f"Write a tweet about: {topic}"

    response = await client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=100
    )

    content = response.choices[0].message.content.strip()
    return {
        "content": content,
        "store_in_memory": True  # Always store tweets in memory
    }