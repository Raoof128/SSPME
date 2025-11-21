# SaaS Security Posture Management (SSPM) Engine

A comprehensive, enterprise-grade security scanning engine for Slack, GitHub, and Google Workspace.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/sspm-engine/sspm-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/sspm-engine/sspm-engine/actions)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📖 Table of Contents

*   [Features](#-features)
*   [Architecture](#-architecture)
*   [Installation](#-installation)
*   [Usage](#-usage)
*   [Configuration](#-configuration)
*   [Development](#-development)
*   [Contributing](#-contributing)

## 🚀 Features

*   **Multi-SaaS Support**: Native integrations for **Slack**, **GitHub**, and **Google Workspace**.
*   **Risk Detection**: Identifies excessive permissions, public resources, misconfigurations, and external sharing.
*   **Secret Scanning**: Built-in regex-based detection for leaked API keys and secrets.
*   **Risk Scoring**: Sophisticated risk engine that calculates scores based on finding severity and asset value.
*   **Reporting**: Generates professional **Markdown** audit reports and JSON summaries for SIEM ingestion.
*   **Dual Interface**: Use via **CLI** for ad-hoc scans or **REST API** for integrations.

## 🏗 Architecture

For a deep dive into the system design, see [ARCHITECTURE.md](ARCHITECTURE.md).

The project uses a standard Python package structure:

*   `sspm_engine/`: Core package source.
    *   `integrations/`: Connectors for SaaS APIs.
    *   `scanners/`: Logic to detect specific risks.
    *   `analytics/`: Risk scoring engine.
    *   `reporting/`: Report generation.
    *   `api/`: FastAPI server.
    *   `cli/`: CLI tool.
*   `tests/`: Test suite.
*   `config/`: Default configurations.

## 📦 Installation

### Prerequisites
*   Python 3.9+
*   Docker (optional)

### Local Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/sspm-engine.git
    cd sspm-engine
    ```

2.  **Install the package:**
    ```bash
    pip install -e .
    ```
    This installs the `sspm-engine` package and the `sspmctl` CLI tool in editable mode.

## 🛠 Usage

### CLI Tool (`sspmctl`)

The Command Line Interface is the quickest way to run scans.

```bash
# Scan all configured providers
sspmctl scan all

# Scan a specific provider
sspmctl scan github

# Generate a full report
sspmctl report --format markdown
```

### API Server

Start the REST API server:

```bash
uvicorn sspm_engine.api.server:app --reload
```

Documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).
See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for details.

## ⚙ Configuration

Configuration is managed via `sspm_engine/config/settings.yaml`.

### Environment Variables

To scan real environments, set the following variables:

```bash
export SLACK_BOT_TOKEN="xoxb-..."
export GITHUB_TOKEN="ghp_..."
export GOOGLE_SA_KEY_PATH="/path/to/service-account.json"
```

If these are not provided, the engine automatically uses **Mock Data** for demonstration purposes.

## 💻 Development

We welcome contributions! Please see:
*   [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
*   [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards.

### Setup Dev Environment

```bash
pip install -r requirements-dev.txt
pre-commit install
```

### Running Tests

```bash
pytest tests/
```

### Building Docker Image

```bash
docker build -t sspm-engine .
docker run -p 8000:8000 sspm-engine
```

## 🛡 Security

Found a vulnerability? Please review our [Security Policy](SECURITY.md) for reporting instructions.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
