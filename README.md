# 🔒 SSPM Engine

<div align="center">

**Enterprise-Grade SaaS Security Posture Management**

[![CI](https://github.com/Raoof128/SSPME/actions/workflows/ci.yml/badge.svg)](https://github.com/Raoof128/SSPME/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)

[Features](#-features) •
[Quick Start](#-quick-start) •
[Documentation](#-documentation) •
[Contributing](#-contributing) •
[License](#-license)

</div>

---

## 📖 Overview

SSPM Engine is a comprehensive, production-ready security scanning platform for SaaS applications. It identifies misconfigurations, excessive permissions, public exposures, and leaked secrets across Slack, GitHub, and Google Workspace.

### Why SSPM Engine?

- **🎯 Multi-SaaS Coverage**: Scan Slack, GitHub, and Google Workspace from a single platform
- **🔍 Comprehensive Detection**: 4 specialized scanners covering permissions, external access, misconfigurations, and secrets
- **📊 Risk Scoring**: Intelligent risk engine with configurable severity rules
- **🚀 Dual Interface**: Use via CLI for ad-hoc scans or REST API for integrations
- **📝 Professional Reports**: Generate Markdown audit reports and JSON for SIEM integration
- **🧪 Mock Data Support**: Test without API credentials using realistic mock data
- **🔐 Security First**: No credential storage, secure logging, type-safe code
- **📚 Production Ready**: Comprehensive documentation, full test coverage, CI/CD pipeline

---

## ✨ Features

### Security Scanners

| Scanner | Detects |
|---------|---------|
| **Permissions** | Admin users without MFA, excessive privileges, risky permission combinations |
| **External Access** | Public repositories, external file sharing, public channels |
| **Misconfigurations** | Missing branch protection, weak security policies, authentication issues |
| **Secrets** | API keys, tokens, passwords, private keys in code and configurations |

### Integrations

- **Slack**: Users, channels, permissions, external guests
- **GitHub**: Repositories, members, branch protection, collaborators
- **Google Workspace**: Users, files, sharing permissions, admin settings

### Reporting

- **Markdown Reports**: Beautiful, human-readable audit reports
- **JSON Reports**: Machine-readable for SIEM/SOAR integration
- **Risk Scoring**: 0-100 scale with severity breakdowns
- **Remediation Guidance**: Actionable steps to fix each finding

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/Raoof128/SSPME.git
cd SSPME

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

### Your First Scan

```bash
# Scan with mock data (no API credentials needed)
python -m sspm_engine.cli.sspmctl scan all

# Generate a report
python -m sspm_engine.cli.sspmctl report --format markdown --output audit.md
```

### With Real Credentials

```bash
# Set environment variables
export SLACK_BOT_TOKEN="xoxb-your-token"
export GITHUB_TOKEN="ghp_your-token"
export GITHUB_ORG="your-organization"
export GOOGLE_SA_KEY_PATH="/path/to/service-account.json"

# Run scan
python -m sspm_engine.cli.sspmctl scan all
```

---

## 📚 Documentation

### Getting Started

- [Installation Guide](docs/INSTALLATION.md) - Detailed installation instructions
- [Quick Start Guide](docs/QUICKSTART.md) - Get up and running in 5 minutes
- [Configuration Guide](docs/CONFIGURATION.md) - API credentials and settings

### Usage

- [Usage Guide](docs/USAGE.md) - CLI commands, API usage, and workflows
- [API Reference](docs/API_REFERENCE.md) - Complete REST API and Python SDK documentation
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions

### Development

- [Contributing Guide](CONTRIBUTING.md) - How to contribute to the project
- [Architecture](ARCHITECTURE.md) - System design and component overview
- [Changelog](CHANGELOG.md) - Version history and release notes

### Policies

- [Security Policy](SECURITY.md) - Security practices and vulnerability reporting
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community guidelines

---

## 💻 Usage Examples

### CLI Usage

```bash
# Scan specific provider
python -m sspm_engine.cli.sspmctl scan slack
python -m sspm_engine.cli.sspmctl scan github
python -m sspm_engine.cli.sspmctl scan google

# Generate reports in different formats
python -m sspm_engine.cli.sspmctl report --format markdown --output audit.md
python -m sspm_engine.cli.sspmctl report --format json --output audit.json

# Check risk score
python -m sspm_engine.cli.sspmctl risk-score
```

### API Usage

```bash
# Start the API server
uvicorn sspm_engine.api.server:app --reload

# Access interactive docs
open http://localhost:8000/docs
```

```bash
# Run scan via API
curl -X POST "http://localhost:8000/scan/all"

# Get risk score
curl "http://localhost:8000/risk-score"
```

### Python SDK Usage

```python
from sspm_engine.engine import SSPMEngine

# Initialize engine
engine = SSPMEngine()

# Run scan
results = engine.run_scan("all")

# Print results
print(f"Risk Score: {results.score}/100")
print(f"Total Findings: {len(results.findings)}")

# Generate report
engine.generate_report(results, format="markdown", output_path="report.md")
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                     │
│         CLI (Typer)              REST API (FastAPI)         │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┼────────────────────────────────────┐
│                        ▼                                    │
│                  SSPM Engine Core                           │
│  • Orchestration  • Configuration  • Error Handling         │
└─────────────────────────────────────────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Integrations   │  │    Scanners     │  │   Analytics     │
│  • Slack        │  │  • Permissions  │  │  • Risk Engine  │
│  • GitHub       │  │  • External     │  │  • Scoring      │
│  • Google WS    │  │  • Misconfig    │  │                 │
│                 │  │  • Secrets      │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design documentation.

---

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=sspm_engine --cov-report=html

# Run specific test
pytest tests/test_permissions.py -v
```

### Code Quality

```bash
# Format code
black .
isort .

# Lint code
flake8 sspm_engine/ tests/

# Type check
mypy sspm_engine/
```

### Building Documentation

```bash
# Install mkdocs
pip install mkdocs mkdocs-material mkdocstrings[python]

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repository
- 📢 Share with others

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 📊 Project Status

- ✅ **Production Ready**: v1.0.0 released
- ✅ **Fully Tested**: Unit and integration tests
- ✅ **Type Safe**: 100% mypy coverage
- ✅ **Well Documented**: Comprehensive guides
- ✅ **CI/CD**: Automated testing and linting
- ✅ **Actively Maintained**: Regular updates

---

## 🔒 Security

Security is our top priority. Please see our [Security Policy](SECURITY.md) for:

- Reporting vulnerabilities
- Security best practices
- Supported versions
- Security features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with ❤️ for the security community
- Inspired by enterprise SSPM solutions
- Powered by open-source technologies

---

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/Raoof128/SSPME/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Raoof128/SSPME/discussions)

---

## 🗺️ Roadmap

### v1.1 (Planned)
- Microsoft 365 integration
- Salesforce integration
- PDF report generation
- Enhanced caching

### v2.0 (Future)
- Web dashboard UI
- Real-time alerting
- ML-based risk prediction
- Historical trend analysis

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

<div align="center">

**Made with ❤️ by the SSPM Engine Team**

[⬆ Back to Top](#-sspm-engine)

</div>
