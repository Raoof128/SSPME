# SSPM Engine Architecture

## Overview

The SSPM (SaaS Security Posture Management) Engine is designed with a modular, extensible architecture that separates concerns and enables easy maintenance and feature additions.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Layer                          │
│  ┌──────────────┐              ┌──────────────────────┐    │
│  │  CLI (Typer) │              │  REST API (FastAPI)  │    │
│  └──────┬───────┘              └──────────┬───────────┘    │
└─────────┼──────────────────────────────────┼────────────────┘
          │                                  │
          └──────────────┬───────────────────┘
                         │
┌────────────────────────┼────────────────────────────────────┐
│                        ▼                                    │
│                  SSPM Engine Core                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Orchestration Layer                      │  │
│  │  • Workflow Management                                │  │
│  │  • Configuration Loading                              │  │
│  │  • Error Handling                                     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Integrations   │  │    Scanners     │  │   Analytics     │
│                 │  │                 │  │                 │
│ • Slack         │  │ • Permissions   │  │ • Risk Engine   │
│ • GitHub        │  │ • External      │  │ • Scoring       │
│ • Google WS     │  │   Access        │  │                 │
│                 │  │ • Misconfig     │  │                 │
│                 │  │ • Secrets       │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
          │                    │                    │
          └────────────────────┼────────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │   Reporting Layer   │
                    │                     │
                    │ • Markdown Reports  │
                    │ • JSON Reports      │
                    │ • Templates         │
                    └─────────────────────┘
```

## Core Components

### 1. Engine Core (`engine.py`)

**Responsibilities:**
- Orchestrates the entire scanning workflow
- Initializes integrations, scanners, and analytics
- Manages configuration loading
- Coordinates data flow between components

**Key Methods:**
- `__init__()`: Initializes all components with configuration
- `run_scan(provider)`: Executes scan workflow
- `generate_report()`: Creates output reports

**Design Pattern:** Facade Pattern - Provides a simplified interface to complex subsystems

### 2. Integrations Layer (`integrations/`)

**Purpose:** Abstract API communication with SaaS providers

**Base Class:** `BaseIntegration`
```python
class BaseIntegration(ABC):
    @abstractmethod
    def connect(self) -> bool
    
    @abstractmethod
    def fetch_data(self) -> Dict[str, List[Any]]
```

**Implementations:**
- `SlackIntegration`: Slack API via slack-sdk
- `GitHubIntegration`: GitHub API via PyGithub
- `GoogleWorkspaceIntegration`: Google Workspace APIs

**Design Pattern:** Strategy Pattern - Interchangeable integration implementations

**Features:**
- Mock data support for testing
- Automatic fallback to mock data when credentials unavailable
- Error handling and retry logic
- Rate limiting compliance

### 3. Scanners Layer (`scanners/`)

**Purpose:** Analyze fetched data for security issues

**Base Class:** `BaseScanner`
```python
class BaseScanner(ABC):
    @abstractmethod
    def scan(self, data: Dict[str, Any]) -> List[Finding]
```

**Implementations:**

#### PermissionsScanner
- Detects excessive admin privileges
- Identifies users without MFA
- Checks for risky permission combinations

#### ExternalAccessScanner
- Finds publicly accessible repositories
- Identifies external file sharing
- Detects public channels/workspaces

#### MisconfigurationScanner
- Checks for missing branch protection
- Validates security policies
- Identifies weak authentication settings

#### SecretScanner
- Regex-based secret detection
- Scans for API keys, tokens, passwords
- Checks repository content and configurations

**Design Pattern:** Strategy Pattern - Pluggable scanner implementations

### 4. Analytics Layer (`analytics/`)

**Components:**

#### RiskEngine (`risk_engine.py`)
- Loads risk rules from configuration
- Enriches findings with severity and category
- Aggregates findings into risk score

#### ScoringEngine (`scoring.py`)
- Calculates numerical risk scores
- Weights findings by severity
- Normalizes scores to 0-100 scale

**Scoring Algorithm:**
```python
score = min(
    sum(severity_weight[finding.severity] for finding in findings),
    100.0
)
```

**Design Pattern:** Chain of Responsibility - Findings flow through analysis pipeline

### 5. Reporting Layer (`reporting/`)

**Purpose:** Generate human and machine-readable reports

**Components:**
- `Reporter`: Main reporting class
- `templates/`: Jinja2 templates for reports
  - `report.md.j2`: Markdown report template
  - `summary.json.j2`: JSON report template

**Output Formats:**
- **Markdown**: Human-readable audit reports
- **JSON**: Machine-readable for SIEM integration

**Design Pattern:** Template Method Pattern - Report structure defined in templates

### 6. Models Layer (`models.py`)

**Purpose:** Define data structures with validation

**Key Models:**

```python
class Finding(BaseModel):
    rule_id: str
    resource_id: str
    resource_type: ResourceType
    details: str
    severity: Severity
    category: str
    data: Optional[Dict[str, Any]]
    remediation: Optional[str]

class ScanResult(BaseModel):
    score: float
    findings: List[Finding]
    counts: Dict[str, int]
```

**Technology:** Pydantic for data validation and serialization

## Data Flow

### Scan Workflow

```
1. User initiates scan (CLI/API)
   ↓
2. Engine loads configuration
   ↓
3. Integrations fetch data from SaaS providers
   ↓
4. Raw data passed to scanners
   ↓
5. Scanners generate findings
   ↓
6. RiskEngine analyzes findings
   ↓
7. ScoringEngine calculates risk score
   ↓
8. Reporter generates output
   ↓
9. Results returned to user
```

### Data Transformation

```
Raw API Data → Normalized Dict → Findings → ScanResult → Report
```

## Configuration Management

### Configuration Files

1. **`config/settings.yaml`**
   - Scanner enable/disable flags
   - Thresholds and limits
   - Custom patterns

2. **`config/risk_rules.json`**
   - Rule definitions
   - Severity mappings
   - Remediation guidance

3. **Environment Variables**
   - API credentials
   - Service account keys
   - Runtime configuration

### Configuration Loading

```python
# Priority order:
1. Environment variables (highest)
2. settings.yaml
3. Default values (lowest)
```

## Error Handling Strategy

### Levels of Error Handling

1. **Integration Level**
   - API connection failures
   - Authentication errors
   - Rate limiting
   - **Action**: Log error, return empty data, continue

2. **Scanner Level**
   - Invalid data format
   - Missing required fields
   - **Action**: Log warning, skip item, continue

3. **Engine Level**
   - Configuration errors
   - Critical failures
   - **Action**: Log error, return partial results or fail gracefully

4. **User Level**
   - Invalid input
   - Missing credentials
   - **Action**: Clear error message, usage guidance

### Logging Strategy

```python
# Structured logging with levels:
- DEBUG: Detailed diagnostic information
- INFO: General informational messages
- WARNING: Non-critical issues
- ERROR: Errors that don't stop execution
- CRITICAL: Fatal errors requiring attention
```

## Security Architecture

### Credential Management

- **Never stored in code**: All credentials from environment
- **No logging**: Credentials never appear in logs
- **Secure transmission**: HTTPS for all API calls
- **Least privilege**: Minimal required API scopes

### Data Protection

- **In-memory processing**: No persistent storage of sensitive data
- **Secure reports**: Reports contain findings, not raw credentials
- **Mock data fallback**: Safe testing without real credentials

## Extensibility Points

### Adding New Integrations

1. Inherit from `BaseIntegration`
2. Implement `connect()` and `fetch_data()`
3. Add to engine initialization
4. Update configuration

### Adding New Scanners

1. Inherit from `BaseScanner`
2. Implement `scan(data)` method
3. Return `List[Finding]`
4. Register in engine

### Adding New Risk Rules

1. Add rule to `config/risk_rules.json`
2. Define severity and category
3. Add remediation guidance
4. Scanner will automatically use new rule

## Performance Considerations

### Optimization Strategies

1. **Parallel API Calls**: Future enhancement for concurrent provider scanning
2. **Caching**: Mock data caching for development
3. **Lazy Loading**: Load integrations only when needed
4. **Streaming**: Process large datasets incrementally

### Scalability

- **Stateless design**: Can be deployed as microservice
- **Horizontal scaling**: Multiple instances can run in parallel
- **Rate limiting**: Respects API limits automatically

## Testing Strategy

### Test Levels

1. **Unit Tests**: Individual components (scanners, integrations)
2. **Integration Tests**: Component interaction
3. **End-to-End Tests**: Full workflow with mock data
4. **Type Checking**: MyPy for type safety

### Mock Data Strategy

- Realistic mock data for each provider
- Covers common security issues
- Enables testing without API access

## Deployment Architecture

### Deployment Options

1. **CLI Tool**: Direct installation via pip
2. **Docker Container**: Isolated environment
3. **API Service**: FastAPI server deployment
4. **Scheduled Jobs**: Cron/systemd for periodic scans

### Environment Configurations

- **Development**: Mock data, debug logging
- **Staging**: Real APIs, verbose logging
- **Production**: Real APIs, minimal logging, monitoring

## Future Enhancements

### Planned Features

1. **Additional Integrations**
   - Microsoft 365
   - Salesforce
   - Zoom
   - Okta

2. **Advanced Analytics**
   - Trend analysis
   - Anomaly detection
   - ML-based risk prediction

3. **Enhanced Reporting**
   - PDF reports
   - Dashboard UI
   - Real-time alerts

4. **Performance**
   - Async/await for parallel scanning
   - Database backend for historical data
   - Caching layer

## Technology Stack

- **Language**: Python 3.9+
- **CLI**: Typer
- **API**: FastAPI
- **Validation**: Pydantic
- **Templates**: Jinja2
- **Testing**: Pytest
- **Type Checking**: MyPy
- **Linting**: Black, Flake8, isort

## Design Principles

1. **Separation of Concerns**: Each component has a single responsibility
2. **Open/Closed Principle**: Open for extension, closed for modification
3. **Dependency Inversion**: Depend on abstractions, not concretions
4. **Interface Segregation**: Small, focused interfaces
5. **Single Responsibility**: Each class has one reason to change

---

**Last Updated**: November 2024

