from typing import List, Dict, Any
from abc import ABC, abstractmethod
from ..models import Finding

class BaseScanner(ABC):
    """
    Abstract base class for security scanners.

    Scanners are responsible for analyzing raw data and identifying security findings.

    Attributes:
        config (Dict[str, Any]): Configuration dictionary for the scanner.
    """
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the scanner.

        Args:
            config (Dict[str, Any]): Configuration dictionary loaded from settings.
        """
        self.config = config

    @abstractmethod
    def scan(self, data: Dict[str, Any]) -> List[Finding]:
        """
        Run the scan logic against the provided data.

        Args:
            data (Dict[str, Any]): The aggregated data collected from integrations.

        Returns:
            List[Finding]: A list of security findings identified by the scanner.
        """
        pass

