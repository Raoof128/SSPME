# Usage Guide

This guide provides comprehensive examples of using the SSPM Engine.

## Table of Contents

- [CLI Usage](#cli-usage)
- [API Usage](#api-usage)
- [Python SDK Usage](#python-sdk-usage)
- [Common Workflows](#common-workflows)
- [Output Formats](#output-formats)

## CLI Usage

The Command Line Interface provides the quickest way to run security scans.

### Basic Scan

Scan all configured providers:

```bash
python -m sspm_engine.cli.sspmctl scan all
```

### Scan Specific Provider

Scan only Slack:

```bash
python -m sspm_engine.cli.sspmctl scan slack
```

Scan only GitHub:

```bash
python -m sspm_engine.cli.sspmctl scan github
```

Scan only Google Workspace:

```bash
python -m sspm_engine.cli.sspmctl scan google
```

### Generate Reports

Generate a Markdown report:

```bash
python -m sspm_engine.cli.sspmctl report --format markdown --output security_audit.md
```

Generate a JSON report:

```bash
python -m sspm_engine.cli.sspmctl report --format json --output security_audit.json
```

### Check Risk Score

Get the current risk score:

```bash
python -m sspm_engine.cli.sspmctl risk-score
```

### Example Output

```
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Severity ┃ Rule            ┃ Resource            ┃ Details                                      ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ HIGH     │ SLACK_NO_MFA    │ admin@company.com   │ Admin user without 2FA enabled               │
│ MEDIUM   │ GH_PUBLIC_REPO  │ company/internal    │ Repository is publicly accessible            │
│ HIGH     │ GW_PUBLIC_DOC   │ Financial_Report.pdf│ Document shared with anyone with the link    │
└──────────┴─────────────────┴─────────────────────┴──────────────────────────────────────────────┘

Risk Score: 65/100
Summary: {'CRITICAL': 0, 'HIGH': 2, 'MEDIUM': 1, 'LOW': 0}
```

## API Usage

The REST API allows programmatic access to the SSPM Engine.

### Start the API Server

```bash
uvicorn sspm_engine.api.server:app --reload --host 0.0.0.0 --port 8000
```

### Health Check

```bash
curl http://localhost:8000/
```

Response:
```json
{
  "status": "ok",
  "message": "SSPM Engine is running"
}
```

### Run a Scan

```bash
curl -X POST "http://localhost:8000/scan/all"
```

Response:
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
      "remediation": "Enable two-factor authentication"
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

### Get Risk Score

```bash
curl http://localhost:8000/risk-score
```

Response:
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

### API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Python SDK Usage

You can also use the SSPM Engine as a Python library.

### Basic Example

```python
from sspm_engine.engine import SSPMEngine

# Initialize the engine
engine = SSPMEngine()

# Run a scan
results = engine.run_scan("all")

# Print results
print(f"Risk Score: {results.score}/100")
print(f"Total Findings: {len(results.findings)}")

# Iterate through findings
for finding in results.findings:
    print(f"[{finding.severity}] {finding.rule_id}: {finding.details}")

# Generate a report
engine.generate_report(results, format="markdown", output_path="report.md")
```

### Scan Specific Provider

```python
from sspm_engine.engine import SSPMEngine

engine = SSPMEngine()

# Scan only GitHub
github_results = engine.run_scan("github")

# Filter critical findings
critical_findings = [
    f for f in github_results.findings 
    if f.severity == "CRITICAL"
]

print(f"Critical Issues: {len(critical_findings)}")
```

### Custom Configuration

```python
from sspm_engine.engine import SSPMEngine

# Use custom config files
engine = SSPMEngine(
    config_path="/path/to/custom/settings.yaml",
    risk_rules_path="/path/to/custom/risk_rules.json"
)

results = engine.run_scan("all")
```

### Access Individual Scanners

```python
from sspm_engine.scanners.permissions import PermissionsScanner
from sspm_engine.scanners.secret_scanner import SecretScanner

# Initialize scanners
config = {"scanners": {"permissions": {"enabled": True}}}
perm_scanner = PermissionsScanner(config)
secret_scanner = SecretScanner(config)

# Prepare data
data = {
    "slack_users": [...],
    "github_repos": [...]
}

# Run specific scanners
perm_findings = perm_scanner.scan(data)
secret_findings = secret_scanner.scan(data)
```

## Common Workflows

### Workflow 1: Daily Security Audit

```bash
#!/bin/bash
# daily_audit.sh

DATE=$(date +%Y-%m-%d)
REPORT_DIR="./security_reports"

mkdir -p $REPORT_DIR

# Run scan and generate report
python -m sspm_engine.cli.sspmctl report \
  --format markdown \
  --output "$REPORT_DIR/audit_$DATE.md"

# Also generate JSON for SIEM integration
python -m sspm_engine.cli.sspmctl report \
  --format json \
  --output "$REPORT_DIR/audit_$DATE.json"

echo "Audit complete: $REPORT_DIR/audit_$DATE.md"
```

### Workflow 2: CI/CD Integration

```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install SSPM Engine
        run: |
          pip install -e .
      
      - name: Run Security Scan
        env:
          SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_ORG: ${{ secrets.GITHUB_ORG }}
        run: |
          python -m sspm_engine.cli.sspmctl report \
            --format json \
            --output security_report.json
      
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: security-report
          path: security_report.json
```

### Workflow 3: Automated Alerting

```python
# alert_on_critical.py
from sspm_engine.engine import SSPMEngine
import smtplib
from email.mime.text import MIMEText

def send_alert(findings):
    msg = MIMEText(f"Critical security issues found: {len(findings)}")
    msg['Subject'] = 'SSPM Alert: Critical Findings'
    msg['From'] = 'security@company.com'
    msg['To'] = 'admin@company.com'
    
    with smtplib.SMTP('localhost') as server:
        server.send_message(msg)

# Run scan
engine = SSPMEngine()
results = engine.run_scan("all")

# Check for critical findings
critical = [f for f in results.findings if f.severity == "CRITICAL"]

if critical:
    send_alert(critical)
    print(f"Alert sent for {len(critical)} critical findings")
else:
    print("No critical findings")
```

### Workflow 4: Compliance Reporting

```python
# compliance_report.py
from sspm_engine.engine import SSPMEngine
from datetime import datetime

engine = SSPMEngine()
results = engine.run_scan("all")

# Generate compliance summary
compliance_data = {
    "report_date": datetime.now().isoformat(),
    "risk_score": results.score,
    "total_findings": len(results.findings),
    "by_severity": results.counts,
    "by_category": {}
}

# Group by category
for finding in results.findings:
    category = finding.category
    if category not in compliance_data["by_category"]:
        compliance_data["by_category"][category] = 0
    compliance_data["by_category"][category] += 1

# Save compliance report
import json
with open("compliance_report.json", "w") as f:
    json.dump(compliance_data, f, indent=2)

print("Compliance report generated")
```

## Output Formats

### Markdown Report

The Markdown report includes:
- Executive summary with risk score
- Severity breakdown
- Detailed findings table
- Remediation recommendations
- Asset inventory

Example:
```markdown
# Security Posture Report

**Generated:** 2024-11-21 12:00:00
**Risk Score:** 65/100

## Executive Summary

- Total Findings: 15
- Critical: 0
- High: 5
- Medium: 8
- Low: 2

## Findings

| Severity | Rule | Resource | Details |
|----------|------|----------|---------|
| HIGH | SLACK_NO_MFA | admin@company.com | Admin without 2FA |
...
```

### JSON Report

The JSON report provides structured data for SIEM integration:

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
      "data": {...},
      "remediation": "Enable two-factor authentication"
    }
  ],
  "counts": {
    "CRITICAL": 0,
    "HIGH": 5,
    "MEDIUM": 8,
    "LOW": 2
  }
}
```

## Best Practices

1. **Schedule Regular Scans**: Run scans daily or weekly to track security posture over time
2. **Automate Reporting**: Integrate with CI/CD pipelines for continuous monitoring
3. **Set Up Alerts**: Configure notifications for critical findings
4. **Track Remediation**: Use reports to track progress on fixing issues
5. **Integrate with SIEM**: Send JSON reports to your security information and event management system

## Troubleshooting

### Issue: Scan takes too long

**Solution:** Scan individual providers separately:
```bash
python -m sspm_engine.cli.sspmctl scan slack &
python -m sspm_engine.cli.sspmctl scan github &
python -m sspm_engine.cli.sspmctl scan google &
wait
```

### Issue: API timeout

**Solution:** Increase timeout in `config/settings.yaml`:
```yaml
api:
  timeout: 300  # 5 minutes
```

## Next Steps

- [Configuration Guide](CONFIGURATION.md) - Customize scanner behavior
- [API Reference](API_REFERENCE.md) - Detailed API documentation
- [Architecture](../ARCHITECTURE.md) - Understand the system design

