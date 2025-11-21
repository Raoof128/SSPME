# Configuration Guide

This guide explains how to configure the SSPM Engine for your environment.

## Configuration Files

### 1. Settings File (`sspm_engine/config/settings.yaml`)

The main configuration file controls scanner behavior and thresholds.

```yaml
scanners:
  permissions:
    enabled: true
    check_admin_users: true
    check_external_collaborators: true
    
  external_access:
    enabled: true
    check_public_repos: true
    check_public_channels: true
    check_shared_files: true
    
  misconfig:
    enabled: true
    check_2fa: true
    check_security_policies: true
    
  secret_scanner:
    enabled: true
    patterns:
      - "api[_-]?key"
      - "secret[_-]?key"
      - "password"
      - "token"

risk_scoring:
  weights:
    CRITICAL: 40
    HIGH: 20
    MEDIUM: 10
    LOW: 5
```

### 2. Risk Rules (`sspm_engine/config/risk_rules.json`)

Defines security rules and their severity levels.

```json
{
  "SLACK_NO_MFA": {
    "severity": "HIGH",
    "category": "authentication",
    "description": "User does not have 2FA enabled",
    "remediation": "Enable two-factor authentication for all users"
  },
  "GH_PUBLIC_REPO": {
    "severity": "MEDIUM",
    "category": "external_access",
    "description": "Repository is publicly accessible",
    "remediation": "Review if repository should be public or make it private"
  }
}
```

## Environment Variables

### Slack Integration

To scan Slack workspaces, you need a Bot Token with appropriate scopes:

```bash
export SLACK_BOT_TOKEN="xoxb-your-slack-bot-token"
```

**Required Scopes:**
- `users:read` - Read user information
- `channels:read` - Read channel information
- `groups:read` - Read private channel information

**How to Get a Token:**
1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Create a new app or select an existing one
3. Navigate to "OAuth & Permissions"
4. Add the required scopes
5. Install the app to your workspace
6. Copy the "Bot User OAuth Token"

### GitHub Integration

To scan GitHub organizations, you need a Personal Access Token:

```bash
export GITHUB_TOKEN="ghp_your-github-personal-access-token"
export GITHUB_ORG="your-organization-name"
```

**Required Permissions:**
- `repo` - Full control of private repositories
- `read:org` - Read organization data
- `admin:org` - Read organization members

**How to Get a Token:**
1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click "Generate new token" → "Generate new token (classic)"
3. Select the required scopes
4. Generate and copy the token

### Google Workspace Integration

To scan Google Workspace, you need a Service Account:

```bash
export GOOGLE_SA_KEY_PATH="/path/to/service-account-key.json"
```

**How to Get Service Account Credentials:**
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Admin SDK API
   - Google Drive API
4. Create a Service Account:
   - Navigate to "IAM & Admin" → "Service Accounts"
   - Click "Create Service Account"
   - Grant appropriate roles
5. Create and download a JSON key
6. Enable domain-wide delegation for the service account
7. In Google Workspace Admin, authorize the service account

**Required OAuth Scopes:**
- `https://www.googleapis.com/auth/admin.directory.user.readonly`
- `https://www.googleapis.com/auth/drive.readonly`

## Using `.env` Files

Create a `.env` file in the project root:

```bash
# .env file
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
GITHUB_TOKEN=ghp_your-github-token
GITHUB_ORG=your-organization
GOOGLE_SA_KEY_PATH=/path/to/service-account.json
```

The engine automatically loads environment variables from `.env` files.

## Mock Data Mode

If no API credentials are provided, the engine uses mock data from `examples/`:

- `examples/mock_slack.json` - Sample Slack data
- `examples/mock_github.json` - Sample GitHub data
- `examples/mock_gw.json` - Sample Google Workspace data

This is useful for:
- Testing the engine without API access
- Demonstrations and training
- Development and debugging

## Advanced Configuration

### Custom Risk Rules

You can add custom rules to `config/risk_rules.json`:

```json
{
  "CUSTOM_RULE_ID": {
    "severity": "CRITICAL",
    "category": "custom_category",
    "description": "Description of the security issue",
    "remediation": "Steps to fix the issue"
  }
}
```

### Scanner Customization

Modify `config/settings.yaml` to enable/disable specific checks:

```yaml
scanners:
  permissions:
    enabled: true
    check_admin_users: true
    admin_threshold: 5  # Alert if more than 5 admins
    
  secret_scanner:
    enabled: true
    custom_patterns:
      - "custom[_-]?pattern"
      - "internal[_-]?key"
```

### Risk Score Weights

Adjust the impact of different severity levels on the overall risk score:

```yaml
risk_scoring:
  weights:
    CRITICAL: 50  # Increase weight for critical findings
    HIGH: 25
    MEDIUM: 10
    LOW: 3
  max_score: 100
```

## Configuration Best Practices

1. **Secure Credentials**: Never commit `.env` files or credentials to version control
2. **Least Privilege**: Grant only the minimum required permissions to API tokens
3. **Rotate Tokens**: Regularly rotate API tokens and service account keys
4. **Audit Logs**: Enable audit logging for all SaaS integrations
5. **Test Configuration**: Use mock data mode to test configuration changes

## Troubleshooting

### Issue: "Authentication failed"

**Solution:** Verify your API tokens are valid and have the required scopes:

```bash
# Test Slack token
curl -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  https://slack.com/api/auth.test

# Test GitHub token
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

### Issue: "Insufficient permissions"

**Solution:** Review the required scopes for each integration and update your tokens accordingly.

### Issue: "Service account not authorized"

**Solution:** Ensure domain-wide delegation is enabled and the service account is authorized in Google Workspace Admin Console.

## Next Steps

- [Usage Guide](USAGE.md) - Learn how to run scans
- [API Reference](API_REFERENCE.md) - Explore the REST API
- [Security Best Practices](../SECURITY.md) - Secure your deployment

