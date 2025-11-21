import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class BaseIntegration(ABC):
    def __init__(self, mock_file: str = None):
        self.mock_file = mock_file

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the SaaS provider."""
        pass

    @abstractmethod
    def fetch_data(self) -> Dict[str, List[Any]]:
        """Fetch all relevant data for scanning."""
        pass
