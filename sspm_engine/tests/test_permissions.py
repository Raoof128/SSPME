import pytest

from sspm_engine.models import Finding, ResourceType
from sspm_engine.scanners.permissions import PermissionsScanner


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
    assert findings[0].rule_id == "SLACK_NO_MFA"
    assert findings[0].resource_type == ResourceType.USER
    assert findings[1].rule_id == "GH_NO_MFA"
