from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ..models import Finding


class BaseScanner(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def scan(self, data: Dict[str, Any]) -> List[Finding]:
        pass
