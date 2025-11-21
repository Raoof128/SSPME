from typing import List, Dict, Any
from ..models import Finding, Severity


class ScoringEngine:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.severity_weights = {
            Severity.CRITICAL: 10.0,
            Severity.HIGH: 7.0,
            Severity.MEDIUM: 4.0,
            Severity.LOW: 1.0,
            Severity.UNKNOWN: 0.0,
        }

    def calculate_score(self, findings: List[Finding]) -> float:
        total_score = 0.0
        for finding in findings:
            weight = self.severity_weights.get(finding.severity, 1.0)
            total_score += weight

        return min(total_score, 100.0)
