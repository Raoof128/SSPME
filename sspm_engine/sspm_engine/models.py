from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"


class ResourceType(str, Enum):
    USER = "user"
    REPO = "repo"
    FILE = "file"
    CHANNEL = "channel"
    UNKNOWN = "unknown"


class Finding(BaseModel):
    rule_id: str
    resource_id: str
    resource_type: ResourceType = ResourceType.UNKNOWN
    details: str
    severity: Severity = Severity.UNKNOWN
    category: str = "general"
    data: Optional[Dict[str, Any]] = None
    remediation: Optional[str] = None


class ScanResult(BaseModel):
    score: float
    findings: List[Finding]
    counts: Dict[str, int]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class User(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    is_admin: bool = False
    has_mfa: bool = False
    source: str


class Repository(BaseModel):
    name: str
    is_private: bool
    branch_protection: bool
    collaborators: List[str] = []
    url: Optional[str] = None
    source: str = "github"


class FileObject(BaseModel):
    id: str
    name: str
    permissions: List[Dict[str, Any]] = []
    publicly_accessible: bool = False
    source: str = "google"
