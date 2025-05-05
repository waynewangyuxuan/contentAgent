import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class Persona:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config["name"]
        self.description = config["description"]
        self.style = config["style"]
        self.traits = config["traits"]
        self.content_preferences = config["content_preferences"]
        self.memory = config["memory"]
        
    def get_system_prompt(self) -> str:
        """Generate a system prompt for the LLM based on persona configuration."""
        prompt = f"""You are {self.name}, {self.description}

Your writing style:
- Tone: {self.style['tone']}
- Length: {self.style['length']}
- Format: {self.style['format']}
- Emojis: {'Use emojis' if self.style['emojis'] else 'No emojis'}
- Jargon: {self.style['jargon']}

Your traits:
{chr(10).join(f"- {trait}" for trait in self.traits)}

Content preferences:
Topics you write about:
{chr(10).join(f"- {topic}" for topic in self.content_preferences['topics'])}

Writing style guidelines:
{chr(10).join(f"- {guideline}" for guideline in self.content_preferences['writing_style'])}
"""
        return prompt

class PersonaManager:
    def __init__(self, profiles_dir: str = "configs/persona_profiles"):
        self.profiles_dir = Path(profiles_dir)
        self.personas: Dict[str, Persona] = {}
        self._load_personas()
        
    def _load_personas(self):
        """Load all persona profiles from the profiles directory."""
        for profile_file in self.profiles_dir.glob("*.yaml"):
            with open(profile_file, 'r') as f:
                config = yaml.safe_load(f)
                persona_name = profile_file.stem
                self.personas[persona_name] = Persona(config)
                
    def get_persona(self, name: str) -> Optional[Persona]:
        """Get a persona by name."""
        return self.personas.get(name)
        
    def list_personas(self) -> Dict[str, str]:
        """List all available personas with their descriptions."""
        return {name: persona.description for name, persona in self.personas.items()} 