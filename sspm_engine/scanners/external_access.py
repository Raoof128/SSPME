from typing import List, Dict, Any
from .base import BaseScanner
from ..models import Finding, ResourceType, Severity


class ExternalAccessScanner(BaseScanner):
    def scan(self, data: Dict[str, Any]) -> List[Finding]:
        findings = []

        # Slack Checks
        slack_users = data.get("slack_users", [])
        for user in slack_users:
            if (
                user.get("is_stranger")
                or user.get("is_restricted")
                or user.get("is_ultra_restricted")
            ):
                findings.append(
                    Finding(
                        rule_id="SLACK_EXT_GUEST",
                        resource_id=f"slack_user:{user.get('name')}",
                        resource_type=ResourceType.USER,
                        details=f"External guest {user.get('name')} found in Slack.",
                        severity=Severity.MEDIUM,
                        category="external_access",
                        data=user,
                    )
                )

        # GitHub Checks
        repos = data.get("github_repos", [])
        for repo in repos:
            if not repo.get("private"):
                findings.append(
                    Finding(
                        rule_id="GH_PUBLIC_REPO",
                        resource_id=f"github_repo:{repo.get('name')}",
                        resource_type=ResourceType.REPO,
                        details=f"Public repository found: {repo.get('name')}",
                        severity=Severity.HIGH,
                        category="external_access",
                        data=repo,
                    )
                )

        # Google Workspace Checks
        gw_files = data.get("google_files", [])
        for file in gw_files:
            for perm in file.get("permissions", []):
                if perm.get("type") == "anyone":
                    findings.append(
                        Finding(
                            rule_id="GW_PUBLIC_DOC",
                            resource_id=f"google_file:{file.get('name')}",
                            resource_type=ResourceType.FILE,
                            details=f"File '{file.get('name')}' is publicly shared.",
                            severity=Severity.HIGH,
                            category="misconfig",
                            data=file,
                        )
                    )

        return findings
