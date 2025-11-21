import re
from typing import Any, Dict, List

from ..models import Finding, ResourceType, Severity
from .base import BaseScanner


class SecretScanner(BaseScanner):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.patterns = {
            "AWS_ACCESS_KEY_ID": r"AKIA[0-9A-Z]{16}",
            "PRIVATE_KEY": r"-----BEGIN PRIVATE KEY-----",
            "GENERIC_API_KEY": r"api_key['\"]?\s*[:=]\s*['\"][a-zA-Z0-9]{32,}['\"]",
        }

    def scan(self, data: Dict[str, Any]) -> List[Finding]:
        findings = []

        for repo in data.get("github_repos", []):
            self._scan_text(
                repo.get("name", ""),
                f"github_repo:{repo.get('name')}",
                ResourceType.REPO,
                findings,
            )

        return findings

    def _scan_text(
        self,
        text: str,
        resource_id: str,
        resource_type: ResourceType,
        findings: List[Finding],
    ):
        for name, pattern in self.patterns.items():
            if re.search(pattern, text):
                findings.append(
                    Finding(
                        rule_id="GH_SECRET_LEAK",
                        resource_id=resource_id,
                        resource_type=resource_type,
                        details=f"Potential {name} found in {resource_id}",
                        severity=Severity.CRITICAL,
                        category="secret_scanner",
                        data={"pattern": name},
                    )
                )
