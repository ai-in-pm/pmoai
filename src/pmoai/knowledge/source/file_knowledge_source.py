import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

from pmoai.knowledge.source.base_file_knowledge_source import BaseFileKnowledgeSource
from pmoai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
from pmoai.knowledge.source.excel_knowledge_source import ExcelKnowledgeSource
from pmoai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from pmoai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from pmoai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource


class FileKnowledgeSource(BaseFileKnowledgeSource):
    """
    A knowledge source that reads from a file.

    This class automatically selects the appropriate knowledge source based on the file extension.
    """

    def __init__(
        self,
        file_path: Union[str, Path],
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        Initialize a file knowledge source.

        Args:
            file_path: The path to the file to read.
            metadata: Optional metadata for this knowledge source.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(file_path=file_path, metadata=metadata, **kwargs)
        self._source = self._get_source()

    def _get_source(self) -> BaseFileKnowledgeSource:
        """
        Get the appropriate knowledge source based on the file extension.

        Returns:
            The appropriate knowledge source.
        """
        file_path = Path(self.file_path)
        extension = file_path.suffix.lower()

        if extension == ".txt":
            return TextFileKnowledgeSource(
                file_path=self.file_path, metadata=self.metadata
            )
        elif extension == ".csv":
            return CSVKnowledgeSource(file_path=self.file_path, metadata=self.metadata)
        elif extension in [".xls", ".xlsx"]:
            return ExcelKnowledgeSource(
                file_path=self.file_path, metadata=self.metadata
            )
        elif extension == ".json":
            return JSONKnowledgeSource(
                file_path=self.file_path, metadata=self.metadata
            )
        elif extension == ".pdf":
            return PDFKnowledgeSource(
                file_path=self.file_path, metadata=self.metadata
            )
        else:
            # Default to text file
            return TextFileKnowledgeSource(
                file_path=self.file_path, metadata=self.metadata
            )

    def get_content(self) -> str:
        """
        Get the content of this knowledge source.

        Returns:
            The content of this knowledge source.
        """
        return self._source.get_content()
