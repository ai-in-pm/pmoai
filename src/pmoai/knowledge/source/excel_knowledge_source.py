from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pmoai.knowledge.source.base_file_knowledge_source import BaseFileKnowledgeSource


class ExcelKnowledgeSource(BaseFileKnowledgeSource):
    """
    A knowledge source that reads from an Excel file.
    """

    def __init__(
        self,
        file_path: Union[str, Path],
        sheet_name: Optional[Union[str, int, List[Union[str, int]]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        Initialize an Excel knowledge source.

        Args:
            file_path: The path to the file to read.
            sheet_name: The name or index of the sheet to read. If None, all sheets are read.
            metadata: Optional metadata for this knowledge source.
            **kwargs: Additional keyword arguments.
        """
        self.sheet_name = sheet_name
        super().__init__(file_path=file_path, metadata=metadata, **kwargs)

    def get_content(self) -> str:
        """
        Get the content of this knowledge source.

        Returns:
            The content of this knowledge source.
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas is required to read Excel files. "
                "Please install it with: pip install pandas openpyxl"
            )

        # Read Excel file
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)

        # If multiple sheets were read, combine them
        if isinstance(df, dict):
            content = ""
            for sheet_name, sheet_df in df.items():
                content += f"Sheet: {sheet_name}\n"
                content += sheet_df.to_string() + "\n\n"
        else:
            content = df.to_string()

        return content
