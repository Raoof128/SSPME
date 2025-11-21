# System Architecture

The SSPM Engine is designed as a modular, extensible platform for auditing SaaS applications.

## High-Level Overview

```mermaid
graph TD
    CLI[CLI Tool] --> Engine
    API[FastAPI Server] --> Engine
    
    subgraph Core Logic
        Engine[SSPM Engine]
        Risk[Risk Engine]
        Scoring[Scoring Engine]
    end
    
    subgraph Integrations
        Slack[Slack Integration]
        GitHub[GitHub Integration]
        Google[Google Integration]
    end
    
    subgraph Scanners
        Perms[Permissions Scanner]
        Ext[External Access Scanner]
        Misconfig[Misconfig Scanner]
        Secret[Secret Scanner]
    end
    
    Engine --> Integrations
    Engine --> Scanners
    Engine --> Risk
    Risk --> Scoring
    
    Integrations --> SaaS[SaaS APIs (Slack, GH, Google)]
    
    Scanners --> Findings[Raw Findings]
    Findings --> Risk
    Risk --> Report[Final Report]
```

## Components

### 1. Core Engine (`engine.py`)
The central orchestrator. It initializes integrations, runs scanners, and invokes the risk engine.

### 2. Integrations (`integrations/`)
Abstracts the complexity of connecting to different SaaS providers.
*   **Slack**: Fetches users, channels.
*   **GitHub**: Fetches repos, members, branch protections.
*   **Google Workspace**: Fetches users, file permissions.

### 3. Scanners (`scanners/`)
Implements specific security checks.
*   **Permissions**: Checks for lack of MFA on admins.
*   **External Access**: Checks for public repos, guests, public docs.
*   **Misconfiguration**: Checks for security settings.
*   **Secret Scanner**: Regex-based secret detection.

### 4. Analytics (`analytics/`)
*   **Risk Engine**: Enriches findings with severity and category based on rules.
*   **Scoring Engine**: Calculates a numerical risk score (0-100).

### 5. Interfaces
*   **CLI (`cli/`)**: Typer-based command line interface.
*   **API (`api/`)**: FastAPI-based REST API.

## Data Flow

1.  User initiates scan via CLI or API.
2.  Engine calls `fetch_data()` on enabled Integrations.
3.  Integrations return normalized data dictionaries.
4.  Engine passes data to all Scanners.
5.  Scanners return a list of `Finding` objects.
6.  Engine passes findings to Risk Engine.
7.  Risk Engine applies rules (`risk_rules.json`) and calculates score.
8.  Result is returned as a `ScanResult` object.
9.  Reporter formats the result into JSON or Markdown.
