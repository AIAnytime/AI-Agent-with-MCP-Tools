import asyncio
import json
import logging
import uuid
from typing import Dict, Any
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from backend.rbac.rbac_manager import RBACManager
from backend.storage.document_storage import DocumentStorage
from backend.mcp.document_tools import DocumentTools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MCP HTTP Server")

TASKS: Dict[str, Dict[str, Any]] = {}

rbac_manager = RBACManager("backend/rbac/model.conf", "backend/rbac/policy.csv")
document_storage = DocumentStorage()
document_tools = DocumentTools(rbac_manager, document_storage)

@app.get("/")
async def root():
    return {"message": "MCP HTTP Server", "status": "running"}

@app.get("/tools/list")
async def list_tools():
    return {
        "tools": document_tools.get_tool_schemas()
    }

@app.post("/tools/call")
async def call_tool_http(request: Request):
    body = await request.json()
    
    user = body.get("user")
    tool = body.get("tool")
    arguments = body.get("arguments", {})
    
    logger.info(f"Tool call: user={user}, tool={tool}, arguments={arguments}")
    
    task_id = str(uuid.uuid4())
    TASKS[task_id] = {
        "status": "running",
        "log": [],
        "result": None
    }
    
    async def run_tool():
        try:
            TASKS[task_id]["log"].append(f"Starting tool: {tool}")
            TASKS[task_id]["log"].append(f"User: {user}")
            TASKS[task_id]["log"].append(f"Arguments: {json.dumps(arguments)}")
            
            if tool == "create_document":
                result = document_tools.create_tool.execute(user, **arguments)
            elif tool == "read_document":
                result = document_tools.read_tool.execute(user, **arguments)
            elif tool == "update_document":
                result = document_tools.update_tool.execute(user, **arguments)
            elif tool == "delete_document":
                result = document_tools.delete_tool.execute(user, **arguments)
            elif tool == "list_documents":
                result = {
                    "status": "success",
                    "data": document_storage.list_documents()
                }
            elif tool == "check_permission":
                action = arguments.get("action")
                has_perm = rbac_manager.check_permission(user, "document", action)
                result = {
                    "status": "success",
                    "has_permission": has_perm,
                    "message": f"User '{user}' {'can' if has_perm else 'cannot'} {action} documents"
                }
            else:
                result = {"status": "error", "message": f"Unknown tool: {tool}"}
            
            TASKS[task_id]["log"].append(f"Tool completed: {result['status']}")
            TASKS[task_id]["result"] = result
            TASKS[task_id]["status"] = "finished"
            
        except Exception as e:
            logger.error(f"Error in tool execution: {str(e)}")
            TASKS[task_id]["status"] = "error"
            TASKS[task_id]["result"] = {"status": "error", "message": str(e)}
            TASKS[task_id]["log"].append(f"Error: {str(e)}")
    
    asyncio.create_task(run_tool())
    
    return {"task_id": task_id}

@app.get("/stream/{task_id}")
async def stream_task(task_id: str):
    async def event_generator():
        last_log_index = 0
        
        while True:
            task = TASKS.get(task_id)
            
            if not task:
                yield {
                    "event": "error",
                    "data": json.dumps({"message": "Task not found"})
                }
                return
            
            if last_log_index < len(task["log"]):
                for log_entry in task["log"][last_log_index:]:
                    yield {
                        "event": "log",
                        "data": json.dumps({"message": log_entry})
                    }
                last_log_index = len(task["log"])
            
            if task["status"] == "finished" or task["status"] == "error":
                yield {
                    "event": "result",
                    "data": json.dumps(task["result"])
                }
                return
            
            await asyncio.sleep(0.2)
    
    return EventSourceResponse(event_generator())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765)
