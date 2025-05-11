import logging
import os
from typing import Any, Dict, List, Optional

from pmoai.memory.storage.interface import Storage


class Mem0Storage(Storage):
    """
    Storage implementation using Mem0 for memory storage.
    """

    def __init__(
        self,
        type: str,
        crew: Optional[Any] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the Mem0 storage.

        Args:
            type: The type of memory (e.g., "short_term", "entities").
            crew: Optional crew instance.
            config: Optional configuration for Mem0.
        """
        try:
            from mem0.client import Mem0Client
        except ImportError:
            raise ImportError(
                "Mem0 is not installed. Please install it with `pip install mem0ai`."
            )

        self.type = type
        self.crew = crew
        self.config = config or {}

        # Initialize Mem0 client
        api_key = os.environ.get("MEM0_API_KEY")
        if not api_key:
            raise ValueError(
                "MEM0_API_KEY environment variable is required for Mem0 storage."
            )

        self.client = Mem0Client(api_key=api_key)
        self.collection_name = self._get_collection_name()

    def _get_collection_name(self) -> str:
        """
        Get the collection name for the memory type.

        Returns:
            The collection name.
        """
        if self.crew:
            crew_name = getattr(self.crew, "name", "")
            return f"{crew_name}_{self.type}" if crew_name else self.type
        return self.type

    def save(self, value: Any, metadata: Dict[str, Any]) -> None:
        """
        Save a memory to Mem0.

        Args:
            value: The memory content.
            metadata: Metadata for the memory.
        """
        try:
            # Add memory to Mem0
            self.client.add_memory(
                memory=str(value),
                collection=self.collection_name,
                metadata=metadata,
            )
        except Exception as e:
            logging.error(f"Error saving memory to Mem0: {e}")

    def search(
        self, query: str, limit: int = 3, score_threshold: float = 0.35
    ) -> List[Dict[str, Any]]:
        """
        Search for memories in Mem0.

        Args:
            query: The search query.
            limit: Maximum number of results to return.
            score_threshold: Minimum score for a result to be included.

        Returns:
            List of memory results.
        """
        try:
            # Search memories in Mem0
            results = self.client.search_memories(
                query=query,
                collection=self.collection_name,
                limit=limit,
                min_relevance_score=score_threshold,
            )

            # Format results to match the expected format
            formatted_results = []
            for result in results:
                formatted_results.append(
                    {
                        "id": result.id,
                        "memory": result.content,
                        "metadata": result.metadata,
                        "score": result.relevance_score,
                    }
                )

            return formatted_results
        except Exception as e:
            logging.error(f"Error searching memories in Mem0: {e}")
            return []

    def reset(self) -> None:
        """
        Reset the Mem0 collection.
        """
        try:
            # Delete all memories in the collection
            self.client.delete_collection(self.collection_name)
        except Exception as e:
            logging.error(f"Error resetting Mem0 collection: {e}")
