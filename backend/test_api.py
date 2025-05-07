from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class TaskRequest(BaseModel):
    task: str
    context: Optional[Dict[str, Any]] = {}

class TaskResponse(BaseModel):
    plan: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    updated_context: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Mock data
available_tools = {
    "search": "Search for information online",
    "fetch_content": "Fetch content from a URL",
    "generate_tweet": "Generate a tweet based on a topic",
    "post_tweet": "Post a tweet to Twitter"
}

memory_stats = {
    "content_count": 42,
    "facts_count": 128
}

# Routes
@app.get("/status")
async def get_status():
    return {
        "status": "active",
        "available_tools": available_tools,
        "memory_stats": memory_stats
    }

@app.post("/task")
async def execute_task(request: TaskRequest):
    # Simulate thinking and processing
    task = request.task.lower()
    context = request.context
    
    # Mock task execution based on keywords
    if "search" in task:
        return {
            "plan": {
                "tool_name": "search",
                "parameters": {"query": task}
            },
            "result": {
                "success": True,
                "data": [
                    {"title": "Example Search Result 1", "snippet": "This is a sample search result."},
                    {"title": "Example Search Result 2", "snippet": "Another sample search result."}
                ]
            },
            "updated_context": {**context, "last_search": task}
        }
    elif "tweet" in task or "post" in task:
        return {
            "plan": {
                "tool_name": "generate_tweet",
                "parameters": {"topic": task}
            },
            "result": {
                "success": True,
                "content": "This is a sample generated tweet about " + task
            },
            "updated_context": {**context, "last_action": "tweet_generation"}
        }
    elif "content" in task or "fetch" in task:
        return {
            "plan": {
                "tool_name": "fetch_content",
                "parameters": {"url": "https://example.com"}
            },
            "result": {
                "success": True,
                "content": "<h1>Example Content</h1><p>This is some example content fetched from a URL.</p>"
            },
            "updated_context": {**context, "last_fetched": "https://example.com"}
        }
    else:
        # Default response for other tasks
        return {
            "plan": {
                "tool_name": "process_text",
                "parameters": {"input": task}
            },
            "result": {
                "success": True,
                "content": f"I processed your request: '{task}'"
            },
            "updated_context": {**context, "last_task": task}
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 