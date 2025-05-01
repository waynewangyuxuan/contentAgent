import os
import aiohttp
from typing import List, Dict

async def search_with_serpapi(query: str, max_results: int = 3) -> List[Dict]:
    """
    Search Google via SerpAPI and return summarized structured results.
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY not set in environment.")

    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": max_results,
    }

    url = "https://serpapi.com/search"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()
                results = data.get("organic_results", [])

                return [
                    {
                        "title": r.get("title"),
                        "snippet": r.get("snippet"),
                        "link": r.get("link")
                    }
                    for r in results[:max_results]
                ]
    except Exception as e:
        print(f"[search_with_serpapi] Search failed: {e}")
        return []