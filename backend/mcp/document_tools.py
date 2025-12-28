import logging
from typing import Dict, Any
from backend.rbac.rbac_manager import RBACManager
from backend.storage.document_storage import DocumentStorage

logger = logging.getLogger(__name__)

class DocumentTool:
    def __init__(self, name: str, action: str, rbac_manager: RBACManager, storage: DocumentStorage):
        self.name = name
        self.action = action
        self.rbac_manager = rbac_manager
        self.storage = storage
    
    def execute(self, user: str, **kwargs) -> Dict[str, Any]:
        if not self.rbac_manager.check_permission(user, "document", self.action):
            return {
                "status": "error",
                "message": f"Permission denied: User '{user}' cannot {self.action} documents"
            }
        
        try:
            if self.action == "create":
                result = self.storage.create_document(
                    kwargs["doc_id"], 
                    kwargs["content"], 
                    user
                )
                return {"status": "success", "message": f"Document '{kwargs['doc_id']}' created", "data": result}
            
            elif self.action == "read":
                result = self.storage.read_document(kwargs["doc_id"])
                return {"status": "success", "data": result}
            
            elif self.action == "update":
                result = self.storage.update_document(
                    kwargs["doc_id"], 
                    kwargs["content"], 
                    user
                )
                return {"status": "success", "message": f"Document '{kwargs['doc_id']}' updated", "data": result}
            
            elif self.action == "delete":
                result = self.storage.delete_document(kwargs["doc_id"], user)
                return result
            
        except Exception as e:
            logger.error(f"Error executing {self.action}: {str(e)}")
            return {"status": "error", "message": str(e)}

class DocumentTools:
    def __init__(self, rbac_manager: RBACManager, storage: DocumentStorage):
        self.create_tool = DocumentTool("create_document", "create", rbac_manager, storage)
        self.read_tool = DocumentTool("read_document", "read", rbac_manager, storage)
        self.update_tool = DocumentTool("update_document", "update", rbac_manager, storage)
        self.delete_tool = DocumentTool("delete_document", "delete", rbac_manager, storage)
    
    def get_tool_schemas(self):
        return [
            {
                "name": "create_document",
                "description": "Create a new document with specified ID and content",
                "parameters": {
                    "doc_id": {"type": "string", "description": "Unique document ID"},
                    "content": {"type": "string", "description": "Document content"}
                }
            },
            {
                "name": "read_document",
                "description": "Read a document by its ID",
                "parameters": {
                    "doc_id": {"type": "string", "description": "Document ID to read"}
                }
            },
            {
                "name": "update_document",
                "description": "Update an existing document with new content",
                "parameters": {
                    "doc_id": {"type": "string", "description": "Document ID to update"},
                    "content": {"type": "string", "description": "New document content"}
                }
            },
            {
                "name": "delete_document",
                "description": "Delete a document by its ID",
                "parameters": {
                    "doc_id": {"type": "string", "description": "Document ID to delete"}
                }
            }
        ]
