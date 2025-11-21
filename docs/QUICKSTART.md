# Quick Start Guide

Get started with the SSPM Engine in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Raoof128/SSPME.git
cd SSPME
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install the Package

```bash
pip install -e .
```

## Your First Scan

### Option 1: Use Mock Data (No API Keys Required)

The engine comes with mock data for demonstration purposes:

```bash
python -m sspm_engine.cli.sspmctl scan all
```

You should see output like this:

```
Starting scan for all...

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

### Option 2: Scan Real Environments

To scan your actual SaaS environments, set up API credentials:

#### For Slack:

```bash
export SLACK_BOT_TOKEN="xoxb-your-slack-bot-token"
```

#### For GitHub:

```bash
export GITHUB_TOKEN="ghp_your-github-token"
export GITHUB_ORG="your-organization"
```

#### For Google Workspace:

```bash
export GOOGLE_SA_KEY_PATH="/path/to/service-account.json"
```

Then run the scan:

```bash
python -m sspm_engine.cli.sspmctl scan all
```

## Generate a Report

Create a comprehensive security report:

```bash
python -m sspm_engine.cli.sspmctl report --format markdown --output security_audit.md
```

View the report:

```bash
cat security_audit.md
```

## Check Your Risk Score

Get a quick overview of your security posture:

```bash
python -m sspm_engine.cli.sspmctl risk-score
```

## Use the REST API

### 1. Start the API Server

```bash
uvicorn sspm_engine.api.server:app --reload
```

### 2. Access the API

Open your browser and navigate to:

- **API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### 3. Run a Scan via API

```bash
curl -X POST "http://localhost:8000/scan/all"
```

## Use as a Python Library

Create a Python script:

```python
# my_scan.py
from sspm_engine.engine import SSPMEngine

# Initialize the engine
engine = SSPMEngine()

# Run a scan
results = engine.run_scan("all")

# Print results
print(f"Risk Score: {results.score}/100")
print(f"Total Findings: {len(results.findings)}")

# Generate a report
engine.generate_report(results, format="markdown", output_path="report.md")
print("Report generated: report.md")
```

Run it:

```bash
python my_scan.py
```

## Common Commands

### Scan specific providers:

```bash
# Scan only Slack
python -m sspm_engine.cli.sspmctl scan slack

# Scan only GitHub
python -m sspm_engine.cli.sspmctl scan github

# Scan only Google Workspace
python -m sspm_engine.cli.sspmctl scan google
```

### Generate different report formats:

```bash
# Markdown report
python -m sspm_engine.cli.sspmctl report --format markdown --output audit.md

# JSON report (for SIEM integration)
python -m sspm_engine.cli.sspmctl report --format json --output audit.json
```

## Docker Quick Start

### Build the Image

```bash
docker build -t sspm-engine .
```

### Run the Container

```bash
docker run -p 8000:8000 sspm-engine
```

Access the API at http://localhost:8000/docs

## Troubleshooting

### Issue: `ModuleNotFoundError`

**Solution:** Make sure you're in the virtual environment:

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

### Issue: `sspmctl: command not found`

**Solution:** Use the module path:

```bash
python -m sspm_engine.cli.sspmctl --help
```

### Issue: API connection errors

**Solution:** If using mock data, this is expected. The engine will automatically use mock data when API credentials are not provided.

## Next Steps

Now that you're up and running, explore these guides:

- **[Configuration Guide](CONFIGURATION.md)** - Set up API credentials and customize settings
- **[Usage Guide](USAGE.md)** - Learn advanced usage patterns
- **[API Reference](API_REFERENCE.md)** - Explore the full API
- **[Architecture](../ARCHITECTURE.md)** - Understand how it works

## Example Use Cases

### 1. Daily Security Audit

```bash
#!/bin/bash
# Run daily at 9 AM via cron
python -m sspm_engine.cli.sspmctl report \
  --format markdown \
  --output "audit_$(date +%Y-%m-%d).md"
```

### 2. CI/CD Integration

```yaml
# .github/workflows/security.yml
- name: Run Security Scan
  run: |
    pip install -e .
    python -m sspm_engine.cli.sspmctl report --format json --output report.json
```

### 3. Compliance Reporting

```python
from sspm_engine.engine import SSPMEngine

engine = SSPMEngine()
results = engine.run_scan("all")

if results.score < 70:
    print("⚠️  Security posture below threshold!")
    exit(1)
else:
    print("✅ Security posture acceptable")
```

## Getting Help

- **Documentation**: https://github.com/Raoof128/SSPME
- **Issues**: https://github.com/Raoof128/SSPME/issues
- **Discussions**: https://github.com/Raoof128/SSPME/discussions

## What's Next?

You've completed the quick start! Here are some suggestions:

1. **Configure API Credentials** - Connect to your real SaaS environments
2. **Customize Risk Rules** - Tailor the engine to your security policies
3. **Set Up Automation** - Schedule regular scans
4. **Integrate with SIEM** - Send JSON reports to your security tools
5. **Contribute** - Help improve the project!

Happy scanning! 🔒

