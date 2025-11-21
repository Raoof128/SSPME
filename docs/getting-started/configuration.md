# Configuration

The SSPM Engine is configured via a combination of **Environment Variables** (for secrets) and **YAML/JSON files** (for rules and settings).

## Environment Variables

Create a `.env` file in the root directory or export these variables in your shell:

| Variable | Description | Required |
|----------|-------------|----------|
| `SLACK_BOT_TOKEN` | Bot User OAuth Token for Slack API | No (uses mock) |
| `GITHUB_TOKEN` | Personal Access Token (PAT) for GitHub API | No (uses mock) |
| `GITHUB_ORG` | GitHub Organization name to scan | No (uses mock) |
| `GOOGLE_SA_KEY_PATH` | Path to Google Service Account JSON key file | No (uses mock) |
| `GOOGLE_ADMIN_EMAIL` | Email of the Google Workspace Admin user | No (uses mock) |

## Settings File (`settings.yaml`)

Located at `config/settings.yaml`. Controls scanning behavior.

```yaml
integrations:
  slack:
    enabled: true
  github:
    enabled: true
  google:
    enabled: true

scanning:
  exclude_repos: []
  exclude_users: []
  secret_regex_patterns:
    - name: "AWS Access Key"
      pattern: "AKIA[0-9A-Z]{16}"
```

## Risk Rules (`risk_rules.json`)

Located at `config/risk_rules.json`. Defines the severity and category of findings.

```json
[
  {
    "id": "SLACK_NO_MFA",
    "name": "Slack Admin without MFA",
    "description": "Administrator account detected without Multi-Factor Authentication.",
    "severity": "HIGH",
    "category": "misconfig"
  }
]
```

