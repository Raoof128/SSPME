# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-21

### Added
- Initial release of SSPM Engine
- Multi-SaaS integration support (Slack, GitHub, Google Workspace)
- Four security scanners:
  - Permissions Scanner (admin privileges, MFA)
  - External Access Scanner (public resources)
  - Misconfiguration Scanner (security policies)
  - Secret Scanner (API keys, tokens)
- Risk scoring engine with configurable rules
- Dual interface: CLI (Typer) and REST API (FastAPI)
- Report generation (Markdown and JSON formats)
- Mock data support for testing without API credentials
- Comprehensive documentation suite
- Full type safety with MyPy
- CI/CD pipeline with GitHub Actions
- Pre-commit hooks for code quality

### Security
- Secure credential management via environment variables
- No credential storage in code or logs
- HTTPS-only API communication
- Input validation with Pydantic
- Type safety enforcement

### Documentation
- Installation guide
- Configuration guide
- Usage examples and workflows
- API reference documentation
- Quick start guide
- Troubleshooting guide
- Contributing guidelines
- Security policy
- Code of conduct
- Architecture documentation

### Testing
- Unit tests for core components
- Integration tests with mock data
- 100% type coverage with MyPy
- Automated linting (Black, Flake8, isort)

## [Unreleased]

### Planned
- Microsoft 365 integration
- Salesforce integration
- Zoom integration
- Okta integration
- PDF report generation
- Web dashboard UI
- Real-time alerting
- Historical trend analysis
- Anomaly detection
- ML-based risk prediction
- Database backend for historical data
- Async/await for parallel scanning
- Enhanced caching layer

---

## Version History

### Version Numbering

We use [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

### Release Types

- **Alpha**: Early development, unstable
- **Beta**: Feature complete, testing phase
- **RC (Release Candidate)**: Final testing before release
- **Stable**: Production-ready release

### Support Policy

- **Latest version**: Full support with security updates
- **Previous minor version**: Security updates only
- **Older versions**: No support

---

[1.0.0]: https://github.com/Raoof128/SSPME/releases/tag/v1.0.0
[Unreleased]: https://github.com/Raoof128/SSPME/compare/v1.0.0...HEAD

