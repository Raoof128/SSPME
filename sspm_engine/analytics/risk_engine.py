import json
from typing import List, Dict, Any
from ..models import Finding, ScanResult, Severity
from .scoring import ScoringEngine

class RiskEngine:
    """
    Analyzes findings to determine severity and calculate risk scores.

    The Risk Engine matches raw findings against configured risk rules to assign
    appropriate severity levels and categories. It also aggregates the total risk score.

    Attributes:
        rules (Dict[str, Dict]): Loaded risk rules indexed by rule ID.
        scorer (ScoringEngine): Instance of the ScoringEngine.
    """
    def __init__(self, rules_file: str):
        """
        Initialize the Risk Engine.

        Args:
            rules_file (str): Path to the JSON file containing risk rules.
        """
        self.rules = self._load_rules(rules_file)
        self.scorer = ScoringEngine()

    def _load_rules(self, path: str) -> Dict[str, Dict]:
        """
        Load risk rules from a JSON file.
        """
        try:
            with open(path, 'r') as f:
                rules_list = json.load(f)
                return {r['id']: r for r in rules_list}
        except Exception as e:
            print(f"Error loading rules: {e}")
            return {}

    def analyze(self, findings: List[Finding]) -> ScanResult:
        """
        Analyze a list of findings.

        Enriches each finding with metadata from the risk rules (severity, category)
        and calculates the overall scan score.

        Args:
            findings (List[Finding]): The list of raw findings from scanners.

        Returns:
            ScanResult: The fully analyzed result containing enriched findings and scores.
        """
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
        """Count findings by severity."""
        counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}
        for f in findings:
            s = f.severity.value
            if s in counts:
                counts[s] += 1
        return counts

