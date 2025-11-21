from typing import List, Dict, Any
from .base import BaseScanner
from ..models import Finding, ResourceType, Severity

class MisconfigurationScanner(BaseScanner):
    def scan(self, data: Dict[str, Any]) -> List[Finding]:
        findings = []

        # GitHub Checks
        repos = data.get("github_repos", [])
        for repo in repos:
            if not repo.get("branch_protection") and not repo.get("private", False) == False: 
                findings.append(Finding(
                    rule_id="GH_NO_BRANCH_PROTECTION",
                    resource_id=f"github_repo:{repo.get('name')}",
                    resource_type=ResourceType.REPO,
                    details=f"Repository {repo.get('name')} does not have branch protection enabled.",
                    severity=Severity.MEDIUM,
                    category="misconfig",
                    data=repo
                ))

        # Google Workspace Checks
        gw_users = data.get("google_users", [])
        for user in gw_users:
            if user.get("is_super_admin") and not user.get("is_enrolled_in_2sv"):
                 findings.append(Finding(
                    rule_id="GW_ADMIN_NO_2SV",
                    resource_id=f"google_user:{user.get('email')}",
                    resource_type=ResourceType.USER,
                    details=f"Super Admin {user.get('email')} is not enrolled in 2SV.",
                    severity=Severity.HIGH,
                    category="misconfig",
                    data=user
                ))

        return findings
