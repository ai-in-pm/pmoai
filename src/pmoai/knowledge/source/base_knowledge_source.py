from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict

from pmoai.knowledge.storage.knowledge_storage import KnowledgeStorage


class BaseKnowledgeSource(ABC, BaseModel):
    """
    Base class for knowledge sources.

    A knowledge source is a source of information that can be added to a knowledge base.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    storage: Optional[KnowledgeStorage] = Field(
        default=None, description="The storage to use for this knowledge source"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadata for this knowledge source"
    )
    chunk_size: int = Field(
        default=1000, description="The size of chunks to split the content into"
    )
    chunk_overlap: int = Field(
        default=200, description="The overlap between chunks"
    )

    @abstractmethod
    def add(self) -> None:
        """
        Add this knowledge source to the knowledge base.
        """
        pass

    @abstractmethod
    def get_content(self) -> str:
        """
        Get the content of this knowledge source.

        Returns:
            The content of this knowledge source.
        """
        pass

    def get_chunks(self) -> List[str]:
        """
        Get the chunks of this knowledge source.

        Returns:
            The chunks of this knowledge source.
        """
        from pmoai.knowledge.utils.knowledge_utils import split_text_into_chunks

        content = self.get_content()
        chunks = split_text_into_chunks(
            content, self.chunk_size, self.chunk_overlap
        )
        return chunks
