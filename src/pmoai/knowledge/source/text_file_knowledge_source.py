from pathlib import Path
from typing import Any, Dict, Optional, Union

from pmoai.knowledge.source.base_file_knowledge_source import BaseFileKnowledgeSource


class TextFileKnowledgeSource(BaseFileKnowledgeSource):
    """
    A knowledge source that reads from a text file.
    """

    def __init__(
        self,
        file_path: Union[str, Path],
        encoding: str = "utf-8",
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        Initialize a text file knowledge source.

        Args:
            file_path: The path to the file to read.
            encoding: The encoding of the file.
            metadata: Optional metadata for this knowledge source.
            **kwargs: Additional keyword arguments.
        """
        self.encoding = encoding
        super().__init__(file_path=file_path, metadata=metadata, **kwargs)

    def get_content(self) -> str:
        """
        Get the content of this knowledge source.

        Returns:
            The content of this knowledge source.
        """
        with open(self.file_path, "r", encoding=self.encoding) as f:
            return f.read()
