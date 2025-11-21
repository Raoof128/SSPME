from typing import List, Dict, Any
from abc import ABC, abstractmethod
from ..models import Finding

class BaseScanner(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def scan(self, data: Dict[str, Any]) -> List[Finding]:
        pass
