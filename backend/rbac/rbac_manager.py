import casbin
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class RBACManager:
    def __init__(self, model_path: str, policy_path: str):
        self.enforcer = casbin.Enforcer(model_path, policy_path)
        logger.info(f"RBAC Manager initialized with model: {model_path}, policy: {policy_path}")
    
    def check_permission(self, user: str, resource: str, action: str) -> bool:
        has_permission = self.enforcer.enforce(user, resource, action)
        
        if has_permission:
            logger.info(f"Permission granted: {user} can {action} on {resource}")
        else:
            logger.warning(f"Permission denied: {user} cannot {action} on {resource}")
        
        return has_permission
    
    def get_user_role(self, user: str) -> str:
        roles = self.enforcer.get_roles_for_user(user)
        return roles[0] if roles else "unknown"
    
    def get_all_users(self):
        subjects = self.enforcer.get_all_subjects()
        users = []
        for subject in subjects:
            if subject not in ['admin', 'editor', 'viewer']:
                role = self.get_user_role(subject)
                users.append({"username": subject, "role": role})
        return users
    
    def get_permissions_for_role(self, role: str):
        permissions = self.enforcer.get_permissions_for_user(role)
        return [{"resource": p[1], "action": p[2]} for p in permissions]
