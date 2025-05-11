import os
from abc import abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import Field

from pmoai.knowledge.source.base_knowledge_source import BaseKnowledgeSource


class BaseFileKnowledgeSource(BaseKnowledgeSource):
    """
    Base class for file-based knowledge sources.

    A file-based knowledge source is a knowledge source that reads from a file.
    """

    file_path: Union[str, Path] = Field(
        ..., description="The path to the file to read"
    )

    def __init__(
        self,
        file_path: Union[str, Path],
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        Initialize a file-based knowledge source.

        Args:
            file_path: The path to the file to read.
            metadata: Optional metadata for this knowledge source.
            **kwargs: Additional keyword arguments.
        """
        if metadata is None:
            metadata = {}

        # Add file metadata
        file_path_obj = Path(file_path)
        if file_path_obj.exists():
            metadata.update(
                {
                    "source": str(file_path_obj),
                    "filename": file_path_obj.name,
                    "filetype": file_path_obj.suffix.lstrip("."),
                    "created": os.path.getctime(file_path_obj),
                    "last_modified": os.path.getmtime(file_path_obj),
                }
            )

        super().__init__(file_path=file_path, metadata=metadata, **kwargs)

    def add(self) -> None:
        """
        Add this knowledge source to the knowledge base.
        """
        if self.storage is None:
            raise ValueError("Storage is not initialized.")

        chunks = self.get_chunks()
        self.storage.add_texts(chunks, self.metadata)

    @abstractmethod
    def get_content(self) -> str:
        """
        Get the content of this knowledge source.

        Returns:
            The content of this knowledge source.
        """
        pass
