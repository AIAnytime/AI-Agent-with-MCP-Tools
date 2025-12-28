import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class DocumentStorage:
    def __init__(self, storage_dir: str = "data/documents"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.storage_dir / "index.json"
        self._load_index()
    
    def _load_index(self):
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                self.index = json.load(f)
        else:
            self.index = {}
            self._save_index()
    
    def _save_index(self):
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)
    
    def create_document(self, doc_id: str, content: str, created_by: str) -> Dict:
        if doc_id in self.index:
            raise ValueError(f"Document '{doc_id}' already exists")
        
        doc_file = self.storage_dir / f"{doc_id}.json"
        doc_data = {
            "id": doc_id,
            "content": content,
            "created_by": created_by,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        with open(doc_file, 'w') as f:
            json.dump(doc_data, f, indent=2)
        
        self.index[doc_id] = {
            "created_by": created_by,
            "created_at": doc_data["created_at"]
        }
        self._save_index()
        
        logger.info(f"Document '{doc_id}' created by {created_by}")
        return doc_data
    
    def read_document(self, doc_id: str) -> Dict:
        if doc_id not in self.index:
            raise ValueError(f"Document '{doc_id}' not found")
        
        doc_file = self.storage_dir / f"{doc_id}.json"
        with open(doc_file, 'r') as f:
            doc_data = json.load(f)
        
        logger.info(f"Document '{doc_id}' read")
        return doc_data
    
    def update_document(self, doc_id: str, content: str, updated_by: str) -> Dict:
        if doc_id not in self.index:
            raise ValueError(f"Document '{doc_id}' not found")
        
        doc_data = self.read_document(doc_id)
        doc_data["content"] = content
        doc_data["updated_at"] = datetime.utcnow().isoformat()
        
        doc_file = self.storage_dir / f"{doc_id}.json"
        with open(doc_file, 'w') as f:
            json.dump(doc_data, f, indent=2)
        
        logger.info(f"Document '{doc_id}' updated by {updated_by}")
        return doc_data
    
    def delete_document(self, doc_id: str, deleted_by: str) -> Dict:
        if doc_id not in self.index:
            raise ValueError(f"Document '{doc_id}' not found")
        
        doc_file = self.storage_dir / f"{doc_id}.json"
        doc_file.unlink()
        
        del self.index[doc_id]
        self._save_index()
        
        logger.info(f"Document '{doc_id}' deleted by {deleted_by}")
        return {"status": "success", "message": f"Document '{doc_id}' deleted"}
    
    def list_documents(self) -> List[Dict]:
        self._load_index()
        documents = []
        for doc_id in self.index.keys():
            try:
                doc_data = self.read_document(doc_id)
                documents.append({
                    "id": doc_data["id"],
                    "created_by": doc_data["created_by"],
                    "created_at": doc_data["created_at"],
                    "updated_at": doc_data["updated_at"],
                    "content_preview": doc_data["content"][:100] + "..." if len(doc_data["content"]) > 100 else doc_data["content"]
                })
            except Exception as e:
                logger.error(f"Error reading document {doc_id}: {e}")
        
        return documents
