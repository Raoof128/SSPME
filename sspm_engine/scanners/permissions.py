from typing import Any, Dict, List

from ..models import Finding, ResourceType, Severity
from .base import BaseScanner


class PermissionsScanner(BaseScanner):
    def scan(self, data: Dict[str, Any]) -> List[Finding]:
        findings = []

        # Slack Checks
        slack_users = data.get("slack_users", [])
        for user in slack_users:
            if user.get("is_admin") and not user.get("has_2fa"):
                user_name = user.get("name")
                findings.append(
                    Finding(
                        rule_id="SLACK_NO_MFA",
                        resource_id=f"slack_user:{user_name}",
                        resource_type=ResourceType.USER,
                        details=(
                            f"Slack Admin {user_name} does not have " "2FA enabled."
                        ),
                        severity=Severity.HIGH,
                        category="misconfig",
                        data=user,
                    )
                )

        # GitHub Checks
        gh_members = data.get("github_members", [])
        for member in gh_members:
            if member.get("role") == "admin" and not member.get("mfa_enabled"):
                member_login = member.get("login")
                findings.append(
                    Finding(
                        rule_id="GH_NO_MFA",
                        resource_id=f"github_user:{member_login}",
                        resource_type=ResourceType.USER,
                        details=(
                            f"GitHub Admin {member_login} does not have " "2FA enabled."
                        ),
                        severity=Severity.HIGH,
                        category="misconfig",
                        data=member,
                    )
                )

        return findings
