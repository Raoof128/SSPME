# API Documentation

The SSPM Engine exposes a RESTful API built with FastAPI.

## Base URL

`http://localhost:8000`

## Endpoints

### Health Check
**GET** `/`
Returns the status of the service.

```json
{
  "status": "ok",
  "message": "SSPM Engine is running"
}
```

### Run Scan
**GET** `/scan/{provider}`

Runs a security scan on the specified provider.

**Parameters:**
*   `provider` (path): `slack`, `github`, `google`, or `all`.

**Response:**
Returns a `ScanResult` object.

```json
{
  "score": 85.0,
  "findings": [
    {
      "rule_id": "GH_PUBLIC_REPO",
      "resource_id": "github_repo:website",
      "resource_type": "repo",
      "details": "Public repository found",
      "severity": "HIGH",
      "category": "external_access"
    }
  ],
  "counts": {
    "CRITICAL": 0,
    "HIGH": 1,
    "MEDIUM": 0,
    "LOW": 0
  }
}
```

### Get Risk Score
**GET** `/risk`

Returns just the high-level risk metrics.

```json
{
  "risk_score": 85.0,
  "counts": { ... }
}
```
