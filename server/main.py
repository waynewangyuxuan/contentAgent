from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import asyncio
import logging
import traceback
from agent.model.planner import Planner
from agent.context.memory import Memory
from agent.registry import ToolRegistry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskRequest(BaseModel):
    task: str
    context: Optional[Dict[str, Any]] = {}

app = FastAPI(title="Content Agent MCP Server")

class AgentServer:
    def __init__(self):
        try:
            self.planner = Planner()
            self.memory = Memory()
            self.tool_registry = ToolRegistry()
            logger.info("Agent server initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize agent server: {str(e)}")
            logger.error(traceback.format_exc())
            raise
        
    async def process_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info(f"Processing task: {task}")
            logger.info(f"Context: {context}")
            
            # 1. Plan next action
            plan = await self.planner.plan(task, context)
            logger.info(f"Plan: {plan}")
            
            # 2. Execute tool
            tool = self.tool_registry.get_tool(plan["tool_name"])
            logger.info(f"Executing tool: {plan['tool_name']}")
            result = await tool.execute(**plan["parameters"])
            logger.info(f"Tool result: {result}")
            
            # 3. Update context with result
            updated_context = self.planner.update_context(context, result)
            
            # 4. Store relevant information in memory
            if result.get("store_in_memory", False):
                self.memory.store_content(
                    content=result["content"],
                    metadata={"task": task, "tool": plan["tool_name"]}
                )
            
            return {
                "plan": plan,
                "result": result,
                "updated_context": updated_context
            }
        except Exception as e:
            logger.error(f"Error processing task: {str(e)}")
            logger.error(traceback.format_exc())
            raise

agent_server = AgentServer()

@app.post("/task")
async def handle_task(request: TaskRequest):
    try:
        result = await agent_server.process_task(request.task, request.context)
        return result
    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    try:
        return {
            "status": "running",
            "available_tools": agent_server.tool_registry.list_tools(),
            "memory_stats": {
                "content_count": len(agent_server.memory.content_collection.get()["ids"]),
                "facts_count": len(agent_server.memory.facts_collection.get()["ids"])
            }
        }
    except Exception as e:
        logger.error(f"Status check failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 