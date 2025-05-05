import os
import aiohttp
from typing import List, Dict
from agent.context.memory import Memory

memory = Memory()  # This will return the singleton instance

async def search_with_serpapi(query: str, max_results: int = 3, num: int = None, engine: str = "google") -> Dict:
    """
    Search via SerpAPI and return structured results.
    
    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 3)
        num: Alternative parameter name for max_results
        engine: Search engine to use (default: "google")
        
    Returns:
        Dictionary containing:
        - results: List of search results, each with title, content, and link
        - query_info: Information about the search query
        - store_in_memory: Boolean indicating if results should be stored
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY not set in environment.")

    # Convert engine to lowercase for consistency
    engine = engine.lower()
    
    # Use num if provided, otherwise use max_results
    results_count = num if num is not None else max_results

    params = {
        "engine": engine,
        "q": query,
        "api_key": api_key,
        "num": results_count,
    }

    url = "https://serpapi.com/search"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()
                results = data.get("organic_results", [])

                # Process results into a clean structure
                search_results = []
                for r in results[:results_count]:
                    search_results.append({
                        "title": r.get("title"),
                        "content": r.get("snippet"),
                        "link": r.get("link")
                    })

                # Generate metadata for memory storage
                metadata = memory.generate_metadata(
                    source="serpapi_search",
                    content_type="search_results",
                    title=f"Search for: {query}",
                    tool="search",
                    additional_metadata={
                        "query": query,
                        "engine": engine,
                        "num_results": len(search_results)
                    }
                )

                return {
                    "results": search_results,
                    "query_info": {
                        "query": query,
                        "engine": engine,
                        "num_results": len(search_results)
                    },
                    "metadata": metadata,
                    "store_in_memory": True
                }
    except Exception as e:
        print(f"[search_with_serpapi] Search failed: {e}")
        return {
            "results": [],
            "query_info": {
                "query": query,
                "engine": engine,
                "error": str(e)
            },
            "metadata": memory.generate_metadata(
                source="serpapi_search",
                content_type="search_error",
                tool="search",
                additional_metadata={"error": str(e)}
            ),
            "store_in_memory": False
        }