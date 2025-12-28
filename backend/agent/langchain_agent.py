import asyncio
import json
import logging
import os
from typing import Dict, Any
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from backend.mcp.mcp_client import MCPClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LangChainMCPAgent:
    def __init__(self, current_user: str = "alice"):
        self.current_user = current_user
        self.mcp_client = None
        self.llm = None
        self.tools = []
        self.agent_executor = None
    
    async def initialize(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            request_timeout=30
        )
        
        self.mcp_client = MCPClient(base_url="http://127.0.0.1:8765")
        try:
            await self.mcp_client.connect()
            logger.info("MCP Client connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            raise
        
        self._create_langchain_tools()
        self._create_react_agent()
        
        logger.info(f"LangChain Agent initialized for user: {self.current_user}")
    
    def _create_langchain_tools(self):
        async def create_document_func(tool_input: str) -> str:
            try:
                params = json.loads(tool_input)
                result = await self.mcp_client.create_document(
                    user=self.current_user,
                    doc_id=params["doc_id"],
                    content=params["content"]
                )
                return json.dumps(result)
            except Exception as e:
                return json.dumps({"status": "error", "message": str(e)})
        
        async def read_document_func(tool_input: str) -> str:
            try:
                params = json.loads(tool_input)
                result = await self.mcp_client.read_document(
                    user=self.current_user,
                    doc_id=params["doc_id"]
                )
                return json.dumps(result)
            except Exception as e:
                return json.dumps({"status": "error", "message": str(e)})
        
        async def update_document_func(tool_input: str) -> str:
            try:
                params = json.loads(tool_input)
                result = await self.mcp_client.update_document(
                    user=self.current_user,
                    doc_id=params["doc_id"],
                    content=params["content"]
                )
                return json.dumps(result)
            except Exception as e:
                return json.dumps({"status": "error", "message": str(e)})
        
        async def delete_document_func(tool_input: str) -> str:
            try:
                params = json.loads(tool_input)
                result = await self.mcp_client.delete_document(
                    user=self.current_user,
                    doc_id=params["doc_id"]
                )
                return json.dumps(result)
            except Exception as e:
                return json.dumps({"status": "error", "message": str(e)})
        
        async def list_documents_func(tool_input: str) -> str:
            try:
                result = await self.mcp_client.list_documents(user=self.current_user)
                return json.dumps(result)
            except Exception as e:
                return json.dumps({"status": "error", "message": str(e)})
        
        async def check_permission_func(tool_input: str) -> str:
            try:
                params = json.loads(tool_input)
                result = await self.mcp_client.check_permission(
                    user=self.current_user,
                    action=params["action"]
                )
                return json.dumps(result)
            except Exception as e:
                return json.dumps({"status": "error", "message": str(e)})
        
        self.tools = [
            Tool(
                name="create_document",
                description='Create a new document. Input must be JSON: {"doc_id": "document-id", "content": "document content"}',
                func=lambda x: asyncio.run(create_document_func(x)),
                coroutine=create_document_func
            ),
            Tool(
                name="read_document",
                description='Read a document by ID. Input must be JSON: {"doc_id": "document-id"}',
                func=lambda x: asyncio.run(read_document_func(x)),
                coroutine=read_document_func
            ),
            Tool(
                name="update_document",
                description='Update an existing document. Input must be JSON: {"doc_id": "document-id", "content": "new content"}',
                func=lambda x: asyncio.run(update_document_func(x)),
                coroutine=update_document_func
            ),
            Tool(
                name="delete_document",
                description='Delete a document by ID. Input must be JSON: {"doc_id": "document-id"}',
                func=lambda x: asyncio.run(delete_document_func(x)),
                coroutine=delete_document_func
            ),
            Tool(
                name="list_documents",
                description='List all documents. Input should be empty JSON: {}',
                func=lambda x: asyncio.run(list_documents_func(x)),
                coroutine=list_documents_func
            ),
            Tool(
                name="check_permission",
                description='Check if current user has permission for an action. Input must be JSON: {"action": "create|read|update|delete"}',
                func=lambda x: asyncio.run(check_permission_func(x)),
                coroutine=check_permission_func
            )
        ]
    
    def _create_react_agent(self):
        react_prompt = PromptTemplate.from_template("""You are an AI assistant for document management with RBAC. Current user: {current_user}

Tools available:
{tools}

You MUST use this exact format:

Question: the input question
Thought: think about what to do next
Action: choose ONE tool from [{tool_names}]
Action Input: provide valid JSON input
Observation: result from the tool

Repeat Thought/Action/Action Input/Observation as needed.

When done:
Thought: I have the final answer
Final Answer: clear response to user

RULES:
1. ALWAYS include "Action:" on its own line after Thought
2. Action Input MUST be valid JSON
3. For list_documents, use: {{}} as input
4. Keep responses concise

Question: {input}
Thought: {agent_scratchpad}""")
        
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=react_prompt
        )
        
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=15,
            handle_parsing_errors=True,
            return_intermediate_steps=False
        )
    
    async def run(self, query: str) -> Dict[str, Any]:
        try:
            result = await self.agent_executor.ainvoke({
                "input": query,
                "current_user": self.current_user
            })
            
            return {
                "status": "success",
                "output": result.get("output", ""),
                "user": self.current_user
            }
        except Exception as e:
            logger.error(f"Agent execution error: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "user": self.current_user
            }
    
    async def cleanup(self):
        if self.mcp_client:
            await self.mcp_client.disconnect()
