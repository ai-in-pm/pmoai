from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

import numpy as np


class BaseKnowledgeStorage(ABC):
    """
    Abstract base class for knowledge storage.

    This class defines the interface for knowledge storage implementations.
    """

    @abstractmethod
    def add_texts(
        self, texts: List[str], metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add texts to the knowledge storage.

        Args:
            texts: List of texts to add.
            metadata: Optional metadata to associate with the texts.
        """
        pass

    @abstractmethod
    def search(
        self,
        query: Union[str, List[str]],
        limit: int = 5,
        score_threshold: float = 0.0,
    ) -> List[Dict[str, Any]]:
        """
        Search for texts in the knowledge storage.

        Args:
            query: Query text or list of query texts.
            limit: Maximum number of results to return.
            score_threshold: Minimum score for a result to be included.

        Returns:
            List of dictionaries containing the search results.
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Reset the knowledge storage.
        """
        pass

    @abstractmethod
    def initialize_knowledge_storage(self) -> None:
        """
        Initialize the knowledge storage.
        """
        pass
