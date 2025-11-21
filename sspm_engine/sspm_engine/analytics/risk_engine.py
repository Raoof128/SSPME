import json
from typing import List, Dict, Any
from ..models import Finding, ScanResult, Severity
from .scoring import ScoringEngine

class RiskEngine:
    def __init__(self, rules_file: str):
        self.rules = self._load_rules(rules_file)
        self.scorer = ScoringEngine()

    def _load_rules(self, path: str) -> Dict[str, Dict]:
        try:
            with open(path, 'r') as f:
                rules_list = json.load(f)
                return {r['id']: r for r in rules_list}
        except Exception as e:
            print(f"Error loading rules: {e}")
            return {}

    def analyze(self, findings: List[Finding]) -> ScanResult:
        enriched_findings = []
        
        for finding in findings:
            rule = self.rules.get(finding.rule_id)
            if rule:
                # Update severity/category from config if it overrides code
                if 'severity' in rule:
                    finding.severity = Severity(rule.get("severity"))
                finding.category = rule.get("category", finding.category)
            
            enriched_findings.append(finding)

        score = self.scorer.calculate_score(enriched_findings)
        counts = self._count_severities(enriched_findings)
        
        return ScanResult(
            score=score,
            findings=enriched_findings,
            counts=counts
        )

    def _count_severities(self, findings: List[Finding]) -> Dict[str, int]:
        counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}
        for f in findings:
            s = f.severity.value
            if s in counts:
                counts[s] += 1
        return counts
