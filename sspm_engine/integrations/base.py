from abc import ABC, abstractmethod
from typing import List, Any, Dict
import logging

logger = logging.getLogger(__name__)

class BaseIntegration(ABC):
    """
    Abstract base class for SaaS integrations.

    All provider integrations (Slack, GitHub, Google, etc.) must inherit from this class
    and implement the `connect` and `fetch_data` methods.

    Attributes:
        mock_file (str, optional): Path to a JSON file containing mock data.
    """
    def __init__(self, mock_file: str = None):
        """
        Initialize the integration.

        Args:
            mock_file (str, optional): Path to a mock data file. If provided, the integration
                should load data from this file instead of making live API calls.
        """
        self.mock_file = mock_file

    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to the SaaS provider.

        Returns:
            bool: True if connection was successful (or using mock), False otherwise.
        """
        pass

    @abstractmethod
    def fetch_data(self) -> Dict[str, List[Any]]:
        """
        Fetch all relevant data for scanning.

        Returns:
            Dict[str, List[Any]]: A dictionary containing lists of resources.
                Example: `{"users": [...], "repos": [...]}`
        """
        pass

