import json
import logging
from typing import Any, Dict, List, Optional

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .base import BaseIntegration

logger = logging.getLogger(__name__)


class SlackIntegration(BaseIntegration):
    def __init__(self, token: Optional[str] = None, mock_file: Optional[str] = None):
        super().__init__(mock_file)
        self.token = token
        self.client: Optional[WebClient] = None

    def connect(self) -> bool:
        if self.token:
            self.client = WebClient(token=self.token)
            return True
        if self.mock_file:
            return True
        return False

    def fetch_data(self) -> Dict[str, List[Any]]:
        data: Dict[str, List[Any]] = {"users": [], "channels": []}

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

    def _get_users(self) -> List[Dict[Any, Any]]:
        try:
            if self.client is None:
                return []
            response = self.client.users_list()
            members: List[Any] = response.get("members", [])
            return list(members) if members else []
        except SlackApiError as e:
            logger.error(f"Slack API User Error: {e}")
            return []

    def _get_channels(self) -> List[Dict[Any, Any]]:
        try:
            if self.client is None:
                return []
            response = self.client.conversations_list(
                types="public_channel,private_channel"
            )
            channels: List[Any] = response.get("channels", [])
            return list(channels) if channels else []
        except SlackApiError as e:
            logger.error(f"Slack API Channel Error: {e}")
            return []

    def _load_mock_data(self):
        try:
            with open(self.mock_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load mock data from {self.mock_file}: {e}")
            return {}
