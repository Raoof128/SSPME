import pytest
import os
from sspm_engine.analytics.risk_engine import RiskEngine
from sspm_engine.models import Finding, Severity, ResourceType

def test_risk_engine():
    # Create a dummy rules file for testing or use existing
    rules_file = "sspm_engine/config/risk_rules.json" 
    assert os.path.exists(rules_file)
    
    engine = RiskEngine(rules_file)
    
    findings = [
        Finding(
            rule_id="SLACK_NO_MFA", 
            resource_id="user:admin", 
            resource_type=ResourceType.USER,
            details="No MFA",
            severity=Severity.UNKNOWN
        ),
        Finding(
            rule_id="UNKNOWN_RULE", 
            resource_id="user:unknown", 
            resource_type=ResourceType.USER,
            details="Unknown",
            severity=Severity.LOW
        )
    ]
    
    result = engine.analyze(findings)
    
    assert result.score > 0
    assert len(result.findings) == 2
    
    # Check that rule enrichment worked (SLACK_NO_MFA is HIGH in rules)
    assert result.findings[0].severity == Severity.HIGH 
    assert result.findings[1].severity == Severity.LOW
