# agent/protocol/local/generator.py

import os
from openai import AsyncOpenAI
from agent.model.persona import PersonaManager
from agent.context.memory import Memory

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
persona_manager = PersonaManager()
memory = Memory()  # This will return the singleton instance

async def generate_tweet(topic: str, persona: str = "classical_critic") -> dict:
    """Generate a tweet about a given topic using the specified persona."""
    # Get the persona configuration
    persona_obj = persona_manager.get_persona(persona)
    if not persona_obj:
        raise ValueError(f"Persona '{persona}' not found")
    
    # Get relevant past content from memory
    past_content = memory.retrieve_relevant_content(topic, n_results=3)
    past_content_str = "\n".join([
        f"Previous content ({c['metadata'].get('title', 'untitled')}): {c['content']}"
        for c in past_content
    ])
    
    # Get the system prompt from the persona
    system_prompt = persona_obj.get_system_prompt()
    user_prompt = f"""Write a tweet about: {topic}

Previous related content:
{past_content_str if past_content else "No previous content found"}

Make sure your tweet is unique and adds new value compared to previous content."""

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
    
    # Generate standardized metadata
    metadata = memory.generate_metadata(
        source="tweet_generation",
        content_type="tweet",
        title=f"Tweet about {topic}",
        task=f"Generate tweet about {topic}",
        tool="generate_tweet",
        additional_metadata={
            "persona": persona,
            "topic": topic
        }
    )
    
    return {
        "content": content,
        "store_in_memory": True,
        "metadata": metadata
    }