import csv
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pmoai.knowledge.source.base_file_knowledge_source import BaseFileKnowledgeSource


class CSVKnowledgeSource(BaseFileKnowledgeSource):
    """
    A knowledge source that reads from a CSV file.
    """

    def __init__(
        self,
        file_path: Union[str, Path],
        encoding: str = "utf-8",
        delimiter: str = ",",
        quotechar: str = '"',
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        Initialize a CSV knowledge source.

        Args:
            file_path: The path to the file to read.
            encoding: The encoding of the file.
            delimiter: The delimiter used in the CSV file.
            quotechar: The quote character used in the CSV file.
            metadata: Optional metadata for this knowledge source.
            **kwargs: Additional keyword arguments.
        """
        self.encoding = encoding
        self.delimiter = delimiter
        self.quotechar = quotechar
        super().__init__(file_path=file_path, metadata=metadata, **kwargs)

    def get_content(self) -> str:
        """
        Get the content of this knowledge source.

        Returns:
            The content of this knowledge source.
        """
        rows = []
        with open(self.file_path, "r", encoding=self.encoding) as f:
            reader = csv.reader(f, delimiter=self.delimiter, quotechar=self.quotechar)
            header = next(reader)
            for row in reader:
                row_dict = {}
                for i, cell in enumerate(row):
                    if i < len(header):
                        row_dict[header[i]] = cell
                rows.append(row_dict)

        # Convert to string
        content = ""
        for row in rows:
            content += str(row) + "\n"

        return content
