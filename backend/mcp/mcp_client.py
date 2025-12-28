import asyncio
import json
import logging
from typing import Dict, Any, Optional
import httpx

logger = logging.getLogger(__name__)

class MCPClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8765"):
        self.base_url = base_url.rstrip("/")
        self.http = None
        self.connected = False
    
    async def connect(self):
        self.http = httpx.AsyncClient(timeout=30.0)
        try:
            response = await self.http.get(f"{self.base_url}/")
            if response.status_code == 200:
                self.connected = True
                logger.info(f"Connected to MCP server at {self.base_url}")
            else:
                logger.error(f"Failed to connect to MCP server: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
    
    async def disconnect(self):
        if self.http:
            await self.http.aclose()
            self.connected = False
    
    async def list_tools(self):
        if not self.connected:
            await self.connect()
        
        response = await self.http.get(f"{self.base_url}/tools/list")
        return response.json()
    
    async def _call_tool_http(self, user: str, tool: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if not self.connected:
            await self.connect()
        
        payload = {
            "user": user,
            "tool": tool,
            "arguments": arguments
        }
        
        response = await self.http.post(f"{self.base_url}/tools/call", json=payload)
        task_id = response.json()["task_id"]
        
        async with self.http.stream("GET", f"{self.base_url}/stream/{task_id}") as resp:
            event_type = None
            async for line in resp.aiter_lines():
                if line.startswith("event:"):
                    event_type = line.replace("event:", "").strip()
                elif line.startswith("data:"):
                    data = line.replace("data:", "").strip()
                    if event_type == "result":
                        return json.loads(data)
                    elif event_type == "log":
                        log_data = json.loads(data)
                        logger.debug(f"MCP Log: {log_data.get('message')}")
        
        return {"status": "error", "message": "No result received"}
    
    async def create_document(self, user: str, doc_id: str, content: str) -> Dict[str, Any]:
        return await self._call_tool_http(user, "create_document", {"doc_id": doc_id, "content": content})
    
    async def read_document(self, user: str, doc_id: str) -> Dict[str, Any]:
        return await self._call_tool_http(user, "read_document", {"doc_id": doc_id})
    
    async def update_document(self, user: str, doc_id: str, content: str) -> Dict[str, Any]:
        return await self._call_tool_http(user, "update_document", {"doc_id": doc_id, "content": content})
    
    async def delete_document(self, user: str, doc_id: str) -> Dict[str, Any]:
        return await self._call_tool_http(user, "delete_document", {"doc_id": doc_id})
    
    async def list_documents(self, user: str) -> Dict[str, Any]:
        return await self._call_tool_http(user, "list_documents", {})
    
    async def check_permission(self, user: str, action: str) -> Dict[str, Any]:
        return await self._call_tool_http(user, "check_permission", {"action": action})
