# Usage Guide

## Command Line Interface (CLI)

The `sspmctl` command is the primary way to interact with the engine.

### Run a Scan

To scan all configured providers:

```bash
sspmctl scan all
```

To scan a specific provider:

```bash
sspmctl scan slack
sspmctl scan github
sspmctl scan google
```

### Generate Reports

After running a scan, you can generate a report in Markdown or JSON format.

```bash
sspmctl report --format markdown --output report.md
sspmctl report --format json --output report.json
```

### Check Risk Score

To see the current risk score without a full report:

```bash
sspmctl risk-score
```

## REST API

The engine provides a FastAPI-based REST interface.

### Start the Server

```bash
uvicorn sspm_engine.api.server:app --reload --host 0.0.0.0 --port 8000
```

### Endpoints

*   `GET /` - Health check
*   `GET /scan/{provider}` - Run a scan and return JSON results
*   `GET /risk` - Get current risk metrics

### Swagger UI

Visit `http://localhost:8000/docs` to interact with the API documentation.

