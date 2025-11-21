import os
import yaml
from typing import Dict, Any

from .integrations.slack import SlackIntegration
from .integrations.github import GitHubIntegration
from .integrations.google_workspace import GoogleWorkspaceIntegration
from .scanners.permissions import PermissionsScanner
from .scanners.external_access import ExternalAccessScanner
from .scanners.misconfig import MisconfigurationScanner
from .scanners.secret_scanner import SecretScanner
from .analytics.risk_engine import RiskEngine
from .reporting.reporter import Reporter
from .models import ScanResult
from .logging_config import setup_logging

logger = setup_logging()

class SSPMEngine:
    """
    Core engine for SaaS Security Posture Management (SSPM).

    This class orchestrates the entire scanning process, including:
    - Initializing integrations (Slack, GitHub, Google Workspace)
    - Configuring scanners
    - Running scans to collect data
    - Analyzing findings with the Risk Engine
    - Generating reports

    Attributes:
        config (Dict[str, Any]): The loaded configuration dictionary.
        risk_engine (RiskEngine): The engine responsible for risk analysis and scoring.
        reporter (Reporter): The reporter instance for generating outputs.
        slack (SlackIntegration): Integration handler for Slack.
        github (GitHubIntegration): Integration handler for GitHub.
        google (GoogleWorkspaceIntegration): Integration handler for Google Workspace.
        scanners (List[BaseScanner]): List of initialized security scanners.
    """
    def __init__(self, config_path: str = None, risk_rules_path: str = None):
        """
        Initialize the SSPM Engine.

        Args:
            config_path (str, optional): Path to the `settings.yaml` configuration file. 
                Defaults to `config/settings.yaml` in the package or project root.
            risk_rules_path (str, optional): Path to the `risk_rules.json` file.
                Defaults to `config/risk_rules.json` in the package or project root.
        """
        base_path = os.path.dirname(os.path.abspath(__file__))
        # Check if running from installed package or source
        # If installed, examples might not be in package dir, so we might need to look elsewhere or expect env vars.
        # For this standalone repo structure, we assume project root is parent of sspm_engine package folder.
        project_root = os.path.dirname(base_path) 
        
        if not config_path:
            config_path = os.path.join(base_path, "config", "settings.yaml")
            if not os.path.exists(config_path):
                config_path = os.path.join(project_root, "config", "settings.yaml")

        if not risk_rules_path:
            risk_rules_path = os.path.join(base_path, "config", "risk_rules.json")
            if not os.path.exists(risk_rules_path):
                risk_rules_path = os.path.join(project_root, "config", "risk_rules.json")

        self.config = self._load_config(config_path)
        self.risk_engine = RiskEngine(risk_rules_path)
        
        template_dir = os.path.join(base_path, "reporting", "templates")
        self.reporter = Reporter(template_dir)
        
        # Initialize Integrations
        mock_dir = os.path.join(project_root, "examples")
        
        self.slack = SlackIntegration(
            token=os.getenv("SLACK_BOT_TOKEN"),
            mock_file=os.path.join(mock_dir, "mock_slack.json") if not os.getenv("SLACK_BOT_TOKEN") else None
        )
        self.github = GitHubIntegration(
            token=os.getenv("GITHUB_TOKEN"),
            org_name=os.getenv("GITHUB_ORG"),
            mock_file=os.path.join(mock_dir, "mock_github.json") if not os.getenv("GITHUB_TOKEN") else None
        )
        self.google = GoogleWorkspaceIntegration(
            credentials_file=os.getenv("GOOGLE_SA_KEY_PATH"),
            mock_file=os.path.join(mock_dir, "mock_gw.json") if not os.getenv("GOOGLE_SA_KEY_PATH") else None
        )

        # Initialize Scanners
        self.scanners = [
            PermissionsScanner(self.config),
            ExternalAccessScanner(self.config),
            MisconfigurationScanner(self.config),
            SecretScanner(self.config)
        ]

    def _load_config(self, path: str) -> Dict[str, Any]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def run_scan(self, provider: str = "all") -> ScanResult:
        """
        Runs a security scan across specified providers.

        This method connects to the configured integrations, fetches data (users, repos, files),
        runs all active scanners against this data, and then passes the findings to the
        Risk Engine for analysis and scoring.

        Args:
            provider (str): The provider to scan. Options are:
                - `"all"`: Scan all configured providers.
                - `"slack"`: Scan only Slack.
                - `"github"`: Scan only GitHub.
                - `"google"`: Scan only Google Workspace.

        Returns:
            ScanResult: An object containing the risk score, list of findings, and severity counts.
        """
        data = {}
        
        # Gather Data
        if provider in ["all", "slack"]:
            logger.info("Fetching Slack data...")
            self.slack.connect()
            slack_data = self.slack.fetch_data()
            data["slack_users"] = slack_data.get("users", [])
            data["slack_channels"] = slack_data.get("channels", [])
            
        if provider in ["all", "github"]:
            logger.info("Fetching GitHub data...")
            self.github.connect()
            gh_data = self.github.fetch_data()
            data["github_repos"] = gh_data.get("repos", [])
            data["github_members"] = gh_data.get("members", [])
            
        if provider in ["all", "google"]:
            logger.info("Fetching Google Workspace data...")
            self.google.connect()
            gw_data = self.google.fetch_data()
            data["google_users"] = gw_data.get("users", [])
            data["google_files"] = gw_data.get("files", [])

        # Run Scanners
        logger.info("Running scanners...")
        all_findings = []
        for scanner in self.scanners:
            all_findings.extend(scanner.scan(data))

        # Analyze Risks
        logger.info("Analyzing risks...")
        analysis = self.risk_engine.analyze(all_findings)
        
        return analysis

    def generate_report(self, analysis: ScanResult, format: str = "markdown", output_path: str = "report.md"):
        """
        Generates a report from the scan results.

        Args:
            analysis (ScanResult): The result object returned by `run_scan`.
            format (str): The desired output format. Options: `"markdown"`, `"json"`. 
                Defaults to `"markdown"`.
            output_path (str): The file path where the report will be saved. 
                Defaults to `"report.md"`.

        Raises:
            ValueError: If an unsupported format is specified (though currently silently ignored/handled by reporter).
        """
        if format == "markdown":
            self.reporter.generate_markdown_report(analysis, output_path)
        elif format == "json":
            self.reporter.generate_json_report(analysis, output_path)
