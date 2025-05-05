import aiohttp
from readability import Document
from typing import Dict, List, Optional
import logging
from agent.context.memory import Memory

logger = logging.getLogger(__name__)
memory = Memory()  # This will return the singleton instance

async def fetch_full_content(url: str) -> Optional[Dict[str, str]]:
    """
    Fetch and extract the main content from a URL and store it in memory.
    
    Args:
        url: The URL to fetch content from
        
    Returns:
        Dictionary containing:
        - title: The page title
        - content: The main content of the page
        - url: The original URL
        - error: Error message if any
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    return {
                        "url": url,
                        "error": f"Failed to fetch content: HTTP {response.status}"
                    }
                
                html = await response.text()
                doc = Document(html)
                
                content = doc.summary()
                title = doc.title()
                
                # Generate standardized metadata
                metadata = memory.generate_metadata(
                    source="web_fetch",
                    content_type="article",
                    title=title,
                    url=url,
                    tool="fetch_content"
                )
                
                # Store in memory
                memory.store_content(
                    content=content,
                    metadata=metadata
                )
                
                return {
                    "title": title,
                    "content": content,
                    "url": url,
                    "metadata": metadata
                }
    except Exception as e:
        logger.error(f"Error fetching content from {url}: {str(e)}")
        return {
            "url": url,
            "error": str(e)
        }

async def fetch_full_contents(urls: List[str]) -> List[Dict[str, str]]:
    """
    Fetch full content from multiple URLs and store them in memory.
    
    Args:
        urls: List of URLs to fetch content from
        
    Returns:
        List of dictionaries containing the content for each URL
    """
    results = []
    for url in urls:
        content = await fetch_full_content(url)
        results.append(content)
    return results 