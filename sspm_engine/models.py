from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class Severity(str, Enum):
    """
    Standardized severity levels for security findings.
    """
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"

class ResourceType(str, Enum):
    """
    Types of resources that can be scanned.
    """
    USER = "user"
    REPO = "repo"
    FILE = "file"
    CHANNEL = "channel"
    UNKNOWN = "unknown"

class Finding(BaseModel):
    """
    Represents a single security issue found during a scan.

    Attributes:
        rule_id (str): Unique identifier for the violated rule.
        resource_id (str): Identifier for the affected resource (e.g., user email, repo name).
        resource_type (ResourceType): The type of resource involved.
        details (str): Human-readable description of the issue.
        severity (Severity): The severity level of the finding.
        category (str): The category of the finding (e.g., "misconfig", "external_access").
        data (Optional[Dict[str, Any]]): Additional raw data related to the finding.
        remediation (Optional[str]): Steps to fix the issue.
    """
    rule_id: str
    resource_id: str
    resource_type: ResourceType = ResourceType.UNKNOWN
    details: str
    severity: Severity = Severity.UNKNOWN
    category: str = "general"
    data: Optional[Dict[str, Any]] = None
    remediation: Optional[str] = None

class ScanResult(BaseModel):
    """
    The aggregate result of a full security scan.

    Attributes:
        score (float): A calculated risk score from 0 to 100.
        findings (List[Finding]): A list of all findings detected.
        counts (Dict[str, int]): A breakdown of finding counts by severity.
        metadata (Dict[str, Any]): Additional metadata about the scan execution.
    """
    score: float
    findings: List[Finding]
    counts: Dict[str, int]
    metadata: Dict[str, Any] = Field(default_factory=dict)

class User(BaseModel):
    """
    Normalized representation of a user across different SaaS platforms.
    """
    id: str
    name: str
    email: Optional[str] = None
    is_admin: bool = False
    has_mfa: bool = False
    source: str

class Repository(BaseModel):
    """
    Normalized representation of a code repository.
    """
    name: str
    is_private: bool
    branch_protection: bool
    collaborators: List[str] = []
    url: Optional[str] = None
    source: str = "github"

class FileObject(BaseModel):
    """
    Normalized representation of a file or document.
    """
    id: str
    name: str
    permissions: List[Dict[str, Any]] = []
    publicly_accessible: bool = False
    source: str = "google"

