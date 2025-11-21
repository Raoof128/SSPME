import pytest
from sspm_engine.scanners.permissions import PermissionsScanner
from sspm_engine.models import Finding, ResourceType, Severity


def test_permissions_scanner():
    scanner = PermissionsScanner({})

    # Mock data with a violation
    data = {
        "slack_users": [
            {"name": "admin", "is_admin": True, "has_2fa": False},
            {"name": "user", "is_admin": False, "has_2fa": False},
        ],
        "github_members": [
            {"login": "admin_gh", "role": "admin", "mfa_enabled": False}
        ],
    }

    findings = scanner.scan(data)

    assert len(findings) == 2
    # Sort findings to ensure deterministic assertion
    findings.sort(key=lambda x: x.rule_id, reverse=True)

    # SLACK_NO_MFA should be first if reverse sorted? No, S comes after G.
    # SLACK > GH.

    assert findings[0].rule_id == "SLACK_NO_MFA"
    assert findings[0].resource_type == ResourceType.USER
    assert findings[1].rule_id == "GH_NO_MFA"
