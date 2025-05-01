import asyncio
import json
import argparse
import aiohttp
from typing import Dict, Any

async def send_task(server_url: str, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server_url}/task",
            json={"task": task, "context": context}
        ) as response:
            return await response.json()

async def get_status(server_url: str) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{server_url}/status") as response:
            return await response.json()

async def main():
    parser = argparse.ArgumentParser(description="Content Agent CLI")
    parser.add_argument("--server", default="http://localhost:8000", help="Server URL")
    parser.add_argument("--task", required=True, help="Task to execute")
    parser.add_argument("--context", default="{}", help="Context JSON string")
    
    args = parser.parse_args()
    
    try:
        context = json.loads(args.context)
    except json.JSONDecodeError:
        print("Error: Invalid context JSON")
        return
    
    try:
        result = await send_task(args.server, args.task, context)
        print("\nTask Result:")
        print(json.dumps(result, indent=2))
        
        status = await get_status(args.server)
        print("\nServer Status:")
        print(json.dumps(status, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 