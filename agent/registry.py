from typing import Dict, Any, Callable, Coroutine
from .protocol.local.generator import generate_tweet
from .protocol.local.search import search_with_serpapi

class Tool:
    def __init__(self, name: str, func: Callable, description: str):
        self.name = name
        self.func = func
        self.description = description
        
    async def execute(self, **kwargs) -> Any:
        """Execute the tool function, handling both sync and async functions."""
        result = self.func(**kwargs)
        if isinstance(result, Coroutine):
            return await result
        return result

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._register_default_tools()
        
    def _register_default_tools(self):
        # Register search tool
        self.register(
            "search",
            search_with_serpapi,
            "Search the web using SerpAPI and return structured results"
        )
        
        # Register generator tool
        self.register(
            "generate_tweet",
            generate_tweet,
            "Generate a tweet about a given topic with a specific persona"
        )
        
    def register(self, name: str, func: Callable, description: str):
        self.tools[name] = Tool(name, func, description)
        
    def get_tool(self, name: str) -> Tool:
        if name not in self.tools:
            raise ValueError(f"Tool {name} not found")
        return self.tools[name]
        
    def list_tools(self) -> Dict[str, str]:
        return {name: tool.description for name, tool in self.tools.items()}
