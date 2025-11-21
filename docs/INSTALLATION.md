# Installation Guide

## Prerequisites

Before installing the SSPM Engine, ensure you have the following:

- **Python 3.9 or higher**
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- **Virtual environment** (recommended)

## Installation Methods

### Method 1: Install from Source (Recommended for Development)

1. **Clone the Repository**

```bash
git clone https://github.com/Raoof128/SSPME.git
cd SSPME
```

2. **Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install the Package**

```bash
pip install -e .
```

This installs the package in editable mode, allowing you to make changes to the code.

4. **Install Development Dependencies** (Optional)

```bash
pip install -e ".[dev]"
```

### Method 2: Install from PyPI (Coming Soon)

```bash
pip install sspm-engine
```

## Verify Installation

Test that the installation was successful:

```bash
python -m sspm_engine.cli.sspmctl --help
```

You should see the CLI help menu with available commands.

## Configuration

### Environment Variables

Create a `.env` file in your project root or set environment variables:

```bash
# Slack Configuration
export SLACK_BOT_TOKEN="xoxb-your-slack-bot-token"

# GitHub Configuration
export GITHUB_TOKEN="ghp_your-github-token"
export GITHUB_ORG="your-organization-name"

# Google Workspace Configuration
export GOOGLE_SA_KEY_PATH="/path/to/service-account.json"
```

### Mock Data Mode

If you don't have API credentials, the engine will automatically use mock data from the `examples/` directory for demonstration purposes.

## Docker Installation (Alternative)

### Build the Docker Image

```bash
docker build -t sspm-engine .
```

### Run the Container

```bash
docker run -p 8000:8000 \
  -e SLACK_BOT_TOKEN="xoxb-..." \
  -e GITHUB_TOKEN="ghp_..." \
  -e GITHUB_ORG="your-org" \
  sspm-engine
```

## Troubleshooting

### Common Issues

#### Issue: `ModuleNotFoundError: No module named 'sspm_engine'`

**Solution:** Ensure you're in the correct directory and have activated your virtual environment:

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

#### Issue: `sspmctl: command not found`

**Solution:** Use the module path instead:

```bash
python -m sspm_engine.cli.sspmctl --help
```

#### Issue: Dependency conflicts

**Solution:** Create a fresh virtual environment:

```bash
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -e .
```

## Next Steps

- Read the [Quick Start Guide](QUICKSTART.md)
- Configure your [API credentials](CONFIGURATION.md)
- Explore [Usage Examples](USAGE.md)
- Review the [API Documentation](API_REFERENCE.md)

## System Requirements

- **Operating System:** Linux, macOS, or Windows
- **RAM:** Minimum 2GB (4GB recommended)
- **Disk Space:** 500MB for installation and dependencies
- **Network:** Internet connection required for API calls to SaaS providers

## Updating

To update to the latest version:

```bash
cd SSPME
git pull origin main
pip install -e . --upgrade
```

