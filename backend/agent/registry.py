from typing import Dict, Any, Callable, Coroutine
from .protocol.local.generator import generate_tweet
from .protocol.local.search import search_with_serpapi
from .protocol.local.content_fetcher import fetch_full_contents
from .protocol.local.twitter import post_tweet
import inspect
import importlib
from .protocol.local import search

class Tool:
    def __init__(self, name: str, func: Callable, description: str):
        self.name = name
        self.func = func
        self.description = description
        self.is_async = inspect.iscoroutinefunction(func)
        
    async def execute(self, **kwargs) -> Any:
        """Execute the tool function, handling both sync and async functions."""
        if self.is_async:
            return await self.func(**kwargs)
        return self.func(**kwargs)

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._register_default_tools()
        
    def _register_default_tools(self):
        # Reload the search module to ensure we have the latest version
        importlib.reload(search)
        
        # Register search tool
        self.register(
            "search",
            search.search_with_serpapi,
            "Search the web using SerpAPI and return structured results."
        )
        
        # Register content fetcher tool
        self.register(
            "fetch_content",
            fetch_full_contents,
            "Fetch and extract the main content from URLs. Can be used to explore interesting topics"
        )
        
        # Register generator tool
        self.register(
            "generate_tweet",
            generate_tweet,
            "Generate a tweet about a given topic with a specific persona based on past content or potential new content"
        )
        
        # Register Twitter posting tool
        self.register(
            "post_tweet",
            post_tweet,
            "Post a tweet with the given text content"
        )
        
    def register(self, name: str, func: Callable, description: str):
        self.tools[name] = Tool(name, func, description)
        
    def get_tool(self, name: str) -> Tool:
        if name not in self.tools:
            raise ValueError(f"Tool {name} not found")
        return self.tools[name]
        
    def list_tools(self) -> Dict[str, str]:
        return {name: tool.description for name, tool in self.tools.items()}
