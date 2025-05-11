from typing import Any, Dict, Optional

from pydantic import Field

from pmoai.knowledge.source.base_knowledge_source import BaseKnowledgeSource


class StringKnowledgeSource(BaseKnowledgeSource):
    """
    A knowledge source that reads from a string.
    """

    content: str = Field(..., description="The content to read")

    def __init__(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        Initialize a string knowledge source.

        Args:
            content: The content to read.
            metadata: Optional metadata for this knowledge source.
            **kwargs: Additional keyword arguments.
        """
        if metadata is None:
            metadata = {}

        # Add string metadata
        metadata.update(
            {
                "source": "string",
                "length": len(content),
            }
        )

        super().__init__(content=content, metadata=metadata, **kwargs)

    def add(self) -> None:
        """
        Add this knowledge source to the knowledge base.
        """
        if self.storage is None:
            raise ValueError("Storage is not initialized.")

        chunks = self.get_chunks()
        self.storage.add_texts(chunks, self.metadata)

    def get_content(self) -> str:
        """
        Get the content of this knowledge source.

        Returns:
            The content of this knowledge source.
        """
        return self.content
