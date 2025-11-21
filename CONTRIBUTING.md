# Contributing to SSPM Engine

Thank you for your interest in contributing to the SSPM Engine! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- **Be respectful** and inclusive
- **Be collaborative** and constructive
- **Focus on what is best** for the community
- **Show empathy** towards other community members

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- GitHub account
- Familiarity with Python, REST APIs, and security concepts

### Finding Issues to Work On

1. **Good First Issues**: Look for issues labeled `good first issue`
2. **Help Wanted**: Check issues labeled `help wanted`
3. **Bug Reports**: Browse open bug reports
4. **Feature Requests**: Review feature requests

## Development Setup

### 1. Fork the Repository

Click the "Fork" button at the top right of the repository page.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/SSPME.git
cd SSPME
```

### 3. Add Upstream Remote

```bash
git remote add upstream https://github.com/Raoof128/SSPME.git
```

### 4. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 5. Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### 6. Install Pre-commit Hooks

```bash
pre-commit install
```

This ensures code quality checks run automatically before each commit.

## How to Contribute

### Reporting Bugs

Before creating a bug report:

1. **Check existing issues** to avoid duplicates
2. **Verify the bug** with the latest version
3. **Collect information** about your environment

When creating a bug report, include:

- **Clear title** describing the issue
- **Steps to reproduce** the bug
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, etc.)
- **Error messages** or logs
- **Screenshots** if applicable

**Example:**

```markdown
**Bug**: CLI hangs when scanning large GitHub organizations

**Steps to Reproduce:**
1. Set GITHUB_ORG to an org with 500+ repos
2. Run `sspmctl scan github`
3. Command hangs after 2 minutes

**Expected**: Scan completes or shows progress
**Actual**: No output, process hangs

**Environment:**
- OS: macOS 12.0
- Python: 3.9.7
- SSPM Engine: 1.0.0
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

1. **Use a clear title** describing the enhancement
2. **Provide detailed description** of the proposed functionality
3. **Explain why** this enhancement would be useful
4. **Provide examples** of how it would work
5. **List alternatives** you've considered

**Example:**

```markdown
**Enhancement**: Add support for Microsoft 365 scanning

**Description:**
Add integration with Microsoft 365 to scan:
- Azure AD users and groups
- SharePoint sites and permissions
- Teams channels and external access

**Motivation:**
Many organizations use Microsoft 365 alongside other SaaS tools.

**Proposed API:**
```python
from sspm_engine.integrations.microsoft import Microsoft365Integration

ms365 = Microsoft365Integration(tenant_id="...", client_id="...")
data = ms365.fetch_data()
```

**Alternatives:**
- Use Microsoft Graph API directly
- Third-party integration tools
```

### Adding New Features

1. **Discuss first**: Open an issue to discuss the feature before coding
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Implement the feature** following coding standards
4. **Add tests** for the new functionality
5. **Update documentation** as needed
6. **Submit a pull request**

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: 88 characters (Black default)
- **Imports**: Sorted with isort
- **Type hints**: Use type hints for function signatures
- **Docstrings**: Google-style docstrings

### Code Formatting

We use automated tools to enforce code style:

- **Black**: Code formatter
- **isort**: Import sorter
- **Flake8**: Linter
- **MyPy**: Type checker

Run formatters before committing:

```bash
black .
isort .
```

Check for issues:

```bash
flake8 .
mypy .
```

### Docstring Format

Use Google-style docstrings:

```python
def scan_provider(provider: str, config: Dict[str, Any]) -> ScanResult:
    """
    Scan a specific SaaS provider for security issues.

    This function initializes the appropriate integration, fetches data,
    and runs all enabled scanners against the data.

    Args:
        provider (str): The provider to scan. Options: "slack", "github", "google".
        config (Dict[str, Any]): Configuration dictionary containing scanner settings.

    Returns:
        ScanResult: Object containing findings, risk score, and severity counts.

    Raises:
        ValueError: If provider is not recognized.
        ConnectionError: If unable to connect to the provider's API.

    Example:
        >>> config = load_config("settings.yaml")
        >>> results = scan_provider("slack", config)
        >>> print(f"Risk Score: {results.score}")
        Risk Score: 65
    """
    # Implementation
    pass
```

### Type Hints

Use type hints for all function signatures:

```python
from typing import List, Dict, Any, Optional

def process_findings(
    findings: List[Finding],
    severity_filter: Optional[Severity] = None
) -> Dict[str, Any]:
    """Process and filter findings."""
    pass
```

### Error Handling

- Use specific exceptions
- Provide helpful error messages
- Log errors appropriately

```python
import logging

logger = logging.getLogger(__name__)

def fetch_data(api_token: str) -> Dict[str, Any]:
    """Fetch data from API."""
    if not api_token:
        raise ValueError("API token is required")
    
    try:
        response = requests.get(API_URL, headers={"Authorization": f"Bearer {api_token}"})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        raise ConnectionError(f"Failed to fetch data: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise ConnectionError(f"Network error: {e}")
```

## Testing

### Running Tests

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=sspm_engine --cov-report=html
```

Run specific test file:

```bash
pytest tests/test_permissions.py
```

Run specific test:

```bash
pytest tests/test_permissions.py::test_admin_without_2fa
```

### Writing Tests

- **Test file naming**: `test_*.py`
- **Test function naming**: `test_*`
- **Use fixtures** for common setup
- **Mock external APIs** to avoid real API calls
- **Test edge cases** and error conditions

**Example:**

```python
import pytest
from unittest.mock import Mock, patch
from sspm_engine.scanners.permissions import PermissionsScanner

@pytest.fixture
def mock_config():
    """Fixture providing test configuration."""
    return {
        "scanners": {
            "permissions": {
                "enabled": True,
                "check_admin_users": True
            }
        }
    }

@pytest.fixture
def scanner(mock_config):
    """Fixture providing initialized scanner."""
    return PermissionsScanner(mock_config)

def test_admin_without_2fa(scanner):
    """Test detection of admin users without 2FA."""
    data = {
        "slack_users": [
            {"name": "admin", "is_admin": True, "has_2fa": False}
        ]
    }
    
    findings = scanner.scan(data)
    
    assert len(findings) == 1
    assert findings[0].rule_id == "SLACK_NO_MFA"
    assert findings[0].severity == "HIGH"

def test_no_findings_when_2fa_enabled(scanner):
    """Test no findings when all admins have 2FA."""
    data = {
        "slack_users": [
            {"name": "admin", "is_admin": True, "has_2fa": True}
        ]
    }
    
    findings = scanner.scan(data)
    
    assert len(findings) == 0

@patch('sspm_engine.integrations.slack.WebClient')
def test_slack_api_error_handling(mock_client, scanner):
    """Test handling of Slack API errors."""
    mock_client.side_effect = Exception("API Error")
    
    with pytest.raises(ConnectionError):
        scanner.scan({"slack_users": []})
```

### Test Coverage

- Aim for **>80% code coverage**
- Test all public APIs
- Test error conditions
- Test edge cases

## Documentation

### Code Documentation

- **Docstrings**: All public classes, methods, and functions must have docstrings
- **Comments**: Explain complex logic, not obvious code
- **Type hints**: Use type hints for clarity

### User Documentation

When adding features, update:

- **README.md**: If it affects installation or basic usage
- **docs/USAGE.md**: For new CLI commands or API endpoints
- **docs/API_REFERENCE.md**: For new classes or methods
- **docs/CONFIGURATION.md**: For new configuration options

### Documentation Format

- Use **Markdown** for all documentation
- Include **code examples** where appropriate
- Add **screenshots** for UI changes
- Keep documentation **up-to-date** with code changes

## Pull Request Process

### Before Submitting

1. **Update your fork**:
```bash
git fetch upstream
git rebase upstream/main
```

2. **Run tests**:
```bash
pytest
```

3. **Run linters**:
```bash
black .
isort .
flake8 .
mypy .
```

4. **Update documentation** if needed

5. **Write a clear commit message**:
```bash
git commit -m "feat: Add Microsoft 365 integration

- Implement Microsoft365Integration class
- Add support for Azure AD user scanning
- Add tests for new integration
- Update documentation

Closes #123"
```

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```
feat(integrations): Add Microsoft 365 support

Implement integration with Microsoft Graph API to scan:
- Azure AD users and groups
- SharePoint permissions
- Teams external access

Closes #123
```

```
fix(cli): Handle timeout errors gracefully

- Add timeout configuration option
- Improve error messages
- Add retry logic with exponential backoff

Fixes #456
```

### Submitting the Pull Request

1. **Push to your fork**:
```bash
git push origin feature/your-feature-name
```

2. **Create pull request** on GitHub

3. **Fill out the PR template**:
   - Description of changes
   - Related issues
   - Testing performed
   - Screenshots (if applicable)

4. **Respond to review feedback**

5. **Keep PR updated** with main branch

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Related Issues
Closes #123

## Changes Made
- Added X feature
- Fixed Y bug
- Updated Z documentation

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed
- [ ] All tests passing

## Documentation
- [ ] Code docstrings added/updated
- [ ] User documentation updated
- [ ] API documentation updated

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review performed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added and passing
- [ ] Dependent changes merged

## Screenshots (if applicable)
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by maintainers
3. **Address feedback** and make changes
4. **Approval** from at least one maintainer
5. **Merge** by maintainer

## Development Workflow

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Keeping Your Fork Updated

```bash
# Fetch latest changes
git fetch upstream

# Merge into your main branch
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

### Rebasing Your Branch

```bash
# Update main first
git checkout main
git pull upstream main

# Rebase your feature branch
git checkout feature/your-feature
git rebase main

# Force push (if already pushed)
git push origin feature/your-feature --force-with-lease
```

## Release Process

Releases are managed by maintainers:

1. **Version bump** in `setup.py` and `pyproject.toml`
2. **Update CHANGELOG.md**
3. **Create release tag**
4. **Publish to PyPI**
5. **Create GitHub release**

## Getting Help

- **Documentation**: Check the [docs/](docs/) directory
- **Issues**: Search existing issues
- **Discussions**: Ask questions in GitHub Discussions
- **Discord**: Join our community Discord (coming soon)

## Recognition

Contributors are recognized in:

- **CONTRIBUTORS.md** file
- **Release notes**
- **GitHub contributors page**

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to SSPM Engine! 🎉

