import json
import logging
from github import Github, GithubException
from typing import Dict, List, Any
from .base import BaseIntegration

logger = logging.getLogger(__name__)

class GitHubIntegration(BaseIntegration):
    def __init__(self, token: str = None, org_name: str = None, mock_file: str = None):
        super().__init__(mock_file)
        self.token = token
        self.org_name = org_name
        self.client = None

    def connect(self) -> bool:
        if self.token:
            self.client = Github(self.token)
            return True
        if self.mock_file:
            return True
        return False

    def fetch_data(self) -> Dict[str, List[Any]]:
        data = {"repos": [], "members": []}
        
        if self.mock_file:
            mock_data = self._load_mock_data()
            data["repos"] = mock_data.get("repos", [])
            data["members"] = mock_data.get("members", [])
            return data

        if not self.client or not self.org_name:
            logger.warning("GitHub client not initialized or Org not set.")
            return data

        try:
            org = self.client.get_organization(self.org_name)
            data["repos"] = self._get_repos(org)
            data["members"] = self._get_members(org)
        except GithubException as e:
            logger.error(f"GitHub API Error: {e}")

        return data

    def _get_repos(self, org) -> List[Dict]:
        repos = []
        for repo in org.get_repos():
            repos.append({
                "name": repo.name,
                "private": repo.private,
                "branch_protection": self._check_branch_protection(repo),
                "collaborators": [c.login for c in repo.get_collaborators()],
                "html_url": repo.html_url
            })
        return repos

    def _get_members(self, org) -> List[Dict]:
        members = []
        for member in org.get_members():
            members.append({
                "login": member.login,
                "role": "member", 
                "mfa_enabled": False 
            })
        return members

    def _check_branch_protection(self, repo):
        try:
            branch = repo.get_branch(repo.default_branch)
            return branch.protected
        except:
            return False

    def _load_mock_data(self):
        try:
            with open(self.mock_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load mock data from {self.mock_file}: {e}")
            return {}
