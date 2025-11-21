# Contributing to SSPM Engine

Thank you for your interest in contributing to the SaaS Security Posture Management (SSPM) Engine! We welcome contributions from the community to help improve security for everyone.

## Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally:
    ```bash
    git clone https://github.com/your-username/sspm-engine.git
    cd sspm-engine
    ```
3.  **Set up the environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -e .
    ```

## Development Workflow

1.  Create a new branch for your feature or bugfix:
    ```bash
    git checkout -b feature/my-awesome-feature
    ```
2.  Write code and add tests.
3.  Run tests to ensure no regressions:
    ```bash
    pytest
    ```
4.  Format your code (we use Black and isort standards).
5.  Commit your changes with clear messages.

## Pull Requests

1.  Push your branch to GitHub.
2.  Open a Pull Request (PR) against the `main` branch.
3.  Describe your changes in detail.
4.  Link any related issues.

## Code Style

*   **Python**: Follow PEP 8.
*   **Type Hints**: Use type hints for all function arguments and return values.
*   **Docstrings**: Document all classes and functions using Google style docstrings.

## Reporting Bugs

Please use the GitHub Issues tab to report bugs. Include:
*   Steps to reproduce.
*   Expected behavior.
*   Actual behavior.
*   Environment details (OS, Python version).
