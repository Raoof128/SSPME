# API Reference

Complete reference for the SSPM Engine REST API and Python SDK.

## Table of Contents

- [REST API](#rest-api)
- [Python SDK](#python-sdk)
- [Data Models](#data-models)
- [Error Handling](#error-handling)

## REST API

### Base URL

```
http://localhost:8000
```

### Authentication

Currently, the API does not require authentication. For production deployments, implement authentication middleware.

### Endpoints

#### GET `/`

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "SSPM Engine is running"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

#### POST `/scan/{provider}`

Run a security scan on the specified provider.

**Parameters:**
- `provider` (path, required): Provider to scan. Options: `all`, `slack`, `github`, `google`

**Example Request:**
```bash
curl -X POST "http://localhost:8000/scan/all"
```

**Response:**
```json
{
  "score": 65,
  "findings": [
    {
      "rule_id": "SLACK_NO_MFA",
      "resource_id": "admin@company.com",
      "resource_type": "user",
      "details": "Admin user without 2FA enabled",
      "severity": "HIGH",
      "category": "authentication",
      "data": {
        "user_id": "U123456",
        "is_admin": true,
        "has_2fa": false
      },
      "remediation": "Enable two-factor authentication for all admin users"
    }
  ],
  "counts": {
    "CRITICAL": 0,
    "HIGH": 2,
    "MEDIUM": 1,
    "LOW": 0
  }
}
```

**Status Codes:**
- `200 OK` - Scan completed successfully
- `400 Bad Request` - Invalid provider specified
- `500 Internal Server Error` - Scan failed

---

#### GET `/risk-score`

Get the current risk score without detailed findings.

**Example Request:**
```bash
curl "http://localhost:8000/risk-score"
```

**Response:**
```json
{
  "score": 65,
  "severity_counts": {
    "CRITICAL": 0,
    "HIGH": 2,
    "MEDIUM": 1,
    "LOW": 0
  }
}
```

**Status Codes:**
- `200 OK` - Risk score calculated successfully
- `500 Internal Server Error` - Calculation failed

---

## Python SDK

### Core Classes

#### `SSPMEngine`

Main orchestration class for running scans and generating reports.

```python
from sspm_engine.engine import SSPMEngine

engine = SSPMEngine(
    config_path: str = None,
    risk_rules_path: str = None
)
```

**Parameters:**
- `config_path` (str, optional): Path to `settings.yaml`. Defaults to `config/settings.yaml`
- `risk_rules_path` (str, optional): Path to `risk_rules.json`. Defaults to `config/risk_rules.json`

**Methods:**

##### `run_scan(provider: str = "all") -> ScanResult`

Run a security scan.

```python
results = engine.run_scan("all")
```

**Parameters:**
- `provider` (str): Provider to scan. Options: `"all"`, `"slack"`, `"github"`, `"google"`

**Returns:**
- `ScanResult`: Object containing findings, score, and severity counts

**Example:**
```python
results = engine.run_scan("github")
print(f"Risk Score: {results.score}")
for finding in results.findings:
    print(f"{finding.severity}: {finding.details}")
```

##### `generate_report(analysis: ScanResult, format: str = "markdown", output_path: str = "report.md")`

Generate a security report.

```python
engine.generate_report(results, format="markdown", output_path="audit.md")
```

**Parameters:**
- `analysis` (ScanResult): Scan results from `run_scan()`
- `format` (str): Output format. Options: `"markdown"`, `"json"`
- `output_path` (str): File path for the report

**Example:**
```python
results = engine.run_scan("all")
engine.generate_report(results, format="json", output_path="report.json")
```

---

### Integration Classes

#### `SlackIntegration`

Slack workspace integration.

```python
from sspm_engine.integrations.slack import SlackIntegration

slack = SlackIntegration(
    token: str = None,
    mock_file: str = None
)
```

**Methods:**

##### `connect()`

Establish connection to Slack API.

##### `fetch_data() -> Dict[str, Any]`

Fetch users and channels from Slack.

**Returns:**
```python
{
    "users": [
        {
            "id": "U123456",
            "name": "john.doe",
            "email": "john@company.com",
            "is_admin": True,
            "has_2fa": False
        }
    ],
    "channels": [
        {
            "id": "C123456",
            "name": "general",
            "is_private": False
        }
    ]
}
```

---

#### `GitHubIntegration`

GitHub organization integration.

```python
from sspm_engine.integrations.github import GitHubIntegration

github = GitHubIntegration(
    token: str = None,
    org_name: str = None,
    mock_file: str = None
)
```

**Methods:**

##### `connect()`

Establish connection to GitHub API.

##### `fetch_data() -> Dict[str, Any]`

Fetch repositories and members from GitHub.

**Returns:**
```python
{
    "repos": [
        {
            "name": "my-repo",
            "private": False,
            "has_security_policy": False
        }
    ],
    "members": [
        {
            "login": "johndoe",
            "role": "admin"
        }
    ]
}
```

---

#### `GoogleWorkspaceIntegration`

Google Workspace integration.

```python
from sspm_engine.integrations.google_workspace import GoogleWorkspaceIntegration

google = GoogleWorkspaceIntegration(
    credentials_file: str = None,
    mock_file: str = None
)
```

**Methods:**

##### `connect()`

Establish connection to Google Workspace APIs.

##### `fetch_data() -> Dict[str, Any]`

Fetch users and files from Google Workspace.

**Returns:**
```python
{
    "users": [
        {
            "email": "john@company.com",
            "is_admin": True,
            "suspended": False
        }
    ],
    "files": [
        {
            "name": "Financial_Report.pdf",
            "permissions": [
                {
                    "type": "anyone",
                    "role": "reader"
                }
            ]
        }
    ]
}
```

---

### Scanner Classes

#### `PermissionsScanner`

Scans for excessive permissions and admin access.

```python
from sspm_engine.scanners.permissions import PermissionsScanner

scanner = PermissionsScanner(config: Dict[str, Any])
findings = scanner.scan(data: Dict[str, Any])
```

**Detects:**
- Admin users without 2FA
- Excessive admin privileges
- External collaborators with admin access

---

#### `ExternalAccessScanner`

Scans for publicly accessible resources.

```python
from sspm_engine.scanners.external_access import ExternalAccessScanner

scanner = ExternalAccessScanner(config: Dict[str, Any])
findings = scanner.scan(data: Dict[str, Any])
```

**Detects:**
- Public GitHub repositories
- Public Slack channels
- Files shared with "anyone with the link"

---

#### `MisconfigurationScanner`

Scans for security misconfigurations.

```python
from sspm_engine.scanners.misconfig import MisconfigurationScanner

scanner = MisconfigurationScanner(config: Dict[str, Any])
findings = scanner.scan(data: Dict[str, Any])
```

**Detects:**
- Missing 2FA enforcement
- Missing security policies
- Weak authentication settings

---

#### `SecretScanner`

Scans for exposed secrets and API keys.

```python
from sspm_engine.scanners.secret_scanner import SecretScanner

scanner = SecretScanner(config: Dict[str, Any])
findings = scanner.scan(data: Dict[str, Any])
```

**Detects:**
- API keys in code
- Passwords in configuration
- Authentication tokens
- Secret keys

---

## Data Models

### `ScanResult`

```python
from sspm_engine.models import ScanResult

class ScanResult:
    score: int  # Risk score (0-100)
    findings: List[Finding]  # List of security findings
    counts: Dict[str, int]  # Count by severity
```

### `Finding`

```python
from sspm_engine.models import Finding, Severity, ResourceType

class Finding:
    rule_id: str  # Unique rule identifier
    resource_id: str  # Affected resource
    resource_type: ResourceType  # Type of resource
    details: str  # Human-readable description
    severity: Severity  # Severity level
    category: str  # Finding category
    data: Optional[Dict[str, Any]]  # Additional data
    remediation: Optional[str]  # Fix instructions
```

### `Severity`

```python
from sspm_engine.models import Severity

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"
```

### `ResourceType`

```python
from sspm_engine.models import ResourceType

class ResourceType(str, Enum):
    USER = "user"
    REPOSITORY = "repository"
    FILE = "file"
    CHANNEL = "channel"
    UNKNOWN = "unknown"
```

---

## Error Handling

### Common Exceptions

#### `ConnectionError`

Raised when unable to connect to a SaaS API.

```python
try:
    engine = SSPMEngine()
    results = engine.run_scan("slack")
except ConnectionError as e:
    print(f"Failed to connect: {e}")
```

#### `AuthenticationError`

Raised when API credentials are invalid.

```python
try:
    slack = SlackIntegration(token="invalid-token")
    slack.connect()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

#### `ConfigurationError`

Raised when configuration files are invalid or missing.

```python
try:
    engine = SSPMEngine(config_path="invalid.yaml")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

### Error Response Format

API errors return JSON with the following structure:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/scan/invalid"
```

Response (400 Bad Request):
```json
{
  "detail": "Invalid provider: invalid. Must be one of: all, slack, github, google"
}
```

---

## Rate Limiting

The SSPM Engine respects API rate limits for each provider:

- **Slack**: 1 request per second
- **GitHub**: 5000 requests per hour
- **Google Workspace**: 100 requests per 100 seconds

When rate limits are exceeded, the engine automatically retries with exponential backoff.

---

## Pagination

For large datasets, the engine automatically handles pagination:

```python
# GitHub repos are automatically paginated
github = GitHubIntegration(token="...", org_name="large-org")
data = github.fetch_data()  # Fetches all repos across multiple pages
```

---

## Webhooks (Coming Soon)

Future versions will support webhooks for real-time alerts:

```python
POST /webhooks/register
{
  "url": "https://your-server.com/webhook",
  "events": ["critical_finding", "scan_complete"]
}
```

---

## Next Steps

- [Usage Guide](USAGE.md) - Learn how to use the API
- [Configuration](CONFIGURATION.md) - Configure the engine
- [Architecture](../ARCHITECTURE.md) - Understand the system design

