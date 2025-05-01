from typing import Dict, Any, List
import json
import logging
import traceback
from openai import OpenAI
import os

logger = logging.getLogger(__name__)

class Planner:
    def __init__(self, model: str = "gpt-4-turbo"):
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set in environment")
            
            self.client = OpenAI(api_key=api_key)
            self.model = model
            logger.info(f"Planner initialized with model: {model}")
        except Exception as e:
            logger.error(f"Failed to initialize planner: {str(e)}")
            logger.error(traceback.format_exc())
            raise
        
    async def plan(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Plan the next action based on the task and context."""
        try:
            system_message = """You are an autonomous content agent that can write high-quality content.
You have access to the following tools:
1. search: Search the web using SerpAPI and return structured results
2. generate_tweet: Generate a tweet about a given topic with a specific persona

Given a task and context, decide which tool to use and what parameters to pass.
Return a JSON object with:
- tool_name: name of the tool to use
- parameters: dict of parameters for the tool
- reasoning: brief explanation of your choice
"""
            
            logger.info(f"Planning task: {task}")
            logger.info(f"Context: {context}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Task: {task}\nContext: {json.dumps(context, indent=2)}"}
                ],
                response_format={"type": "json_object"}
            )
            
            plan = json.loads(response.choices[0].message.content)
            logger.info(f"Generated plan: {plan}")
            return plan
            
        except Exception as e:
            logger.error(f"Error in planning: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def update_context(self, context: Dict[str, Any], result: Any) -> Dict[str, Any]:
        """Update the context based on the result of the last action."""
        try:
            if "last_results" not in context:
                context["last_results"] = []
            context["last_results"].append(result)
            logger.info(f"Updated context: {context}")
            return context
        except Exception as e:
            logger.error(f"Error updating context: {str(e)}")
            logger.error(traceback.format_exc())
            raise
