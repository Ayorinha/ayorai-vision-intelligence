from dataclasses import dataclass
from enum import StrEnum

class Role(StrEnum):
    VIEWER = "viewer"
    ANALYST = "analyst"
    REVIEWER = "reviewer"
    ADMIN = "admin"

@dataclass(frozen=True)
class Principal:
    tenant_id: str
    role: Role

ROLE_PERMISSIONS = {
    Role.VIEWER: {"search_procedure"},
    Role.ANALYST: {"search_procedure", "validate_remessa", "create_review"},
    Role.REVIEWER: {"search_procedure", "validate_remessa", "create_review", "release_remessa"},
    Role.ADMIN: {"search_procedure", "validate_remessa", "create_review", "release_remessa"},
}

def can_call(principal: Principal, tool: str, target_tenant: str) -> bool:
    return principal.tenant_id == target_tenant and tool in ROLE_PERMISSIONS[principal.role]
