import json
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Dict, List, Any
from .base import BaseIntegration
from ..models import User, ResourceType

logger = logging.getLogger(__name__)

class SlackIntegration(BaseIntegration):
    def __init__(self, token: str = None, mock_file: str = None):
        super().__init__(mock_file)
        self.token = token
        self.client = None

    def connect(self) -> bool:
        if self.token:
            self.client = WebClient(token=self.token)
            return True
        if self.mock_file:
            return True
        return False

    def fetch_data(self) -> Dict[str, List[Any]]:
        data = {"users": [], "channels": []}
        
        if self.mock_file:
            mock_data = self._load_mock_data()
            data["users"] = mock_data.get("users", [])
            data["channels"] = mock_data.get("channels", [])
            return data

        if not self.client:
            logger.warning("Slack client not initialized.")
            return data

        try:
            data["users"] = self._get_users()
            data["channels"] = self._get_channels()
        except Exception as e:
            logger.error(f"Error fetching Slack data: {e}")

        return data

    def _get_users(self) -> List[Dict]:
        try:
            response = self.client.users_list()
            return response["members"]
        except SlackApiError as e:
            logger.error(f"Slack API User Error: {e}")
            return []

    def _get_channels(self) -> List[Dict]:
        try:
            response = self.client.conversations_list(types="public_channel,private_channel")
            return response["channels"]
        except SlackApiError as e:
            logger.error(f"Slack API Channel Error: {e}")
            return []

    def _load_mock_data(self):
        try:
            with open(self.mock_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load mock data from {self.mock_file}: {e}")
            return {}
