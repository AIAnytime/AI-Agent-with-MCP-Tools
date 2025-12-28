import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from backend.agent.langchain_agent import LangChainMCPAgent
from backend.rbac.rbac_manager import RBACManager
from backend.storage.document_storage import DocumentStorage

project_root = Path(__file__).parent.parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rbac_manager = RBACManager("backend/rbac/model.conf", "backend/rbac/policy.csv")
document_storage = DocumentStorage()

agents = {}

class QueryRequest(BaseModel):
    query: str
    user: str

class QueryResponse(BaseModel):
    status: str
    output: Optional[str] = None
    message: Optional[str] = None
    user: str

@app.get("/")
async def root():
    return {"message": "AI Agent API", "status": "running"}

@app.get("/users")
async def get_users():
    users = rbac_manager.get_all_users()
    return {"users": users}

@app.get("/permissions/{role}")
async def get_permissions(role: str):
    permissions = rbac_manager.get_permissions_for_role(role)
    return {"role": role, "permissions": permissions}

@app.get("/documents")
async def list_documents():
    documents = document_storage.list_documents()
    return {"documents": documents}

@app.post("/agent/query", response_model=QueryResponse)
async def agent_query(request: QueryRequest):
    try:
        user = request.user
        
        if user not in agents:
            agent = LangChainMCPAgent(current_user=user)
            await agent.initialize()
            agents[user] = agent
        else:
            agent = agents[user]
        
        result = await agent.run(request.query)
        
        return QueryResponse(
            status=result["status"],
            output=result.get("output"),
            message=result.get("message"),
            user=user
        )
    
    except Exception as e:
        logger.error(f"Error in agent query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
async def shutdown_event():
    for agent in agents.values():
        await agent.cleanup()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
