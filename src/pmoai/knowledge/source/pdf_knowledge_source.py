from pathlib import Path
from typing import Any, Dict, Optional, Union

from pmoai.knowledge.source.base_file_knowledge_source import BaseFileKnowledgeSource


class PDFKnowledgeSource(BaseFileKnowledgeSource):
    """
    A knowledge source that reads from a PDF file.
    """

    def __init__(
        self,
        file_path: Union[str, Path],
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        Initialize a PDF knowledge source.

        Args:
            file_path: The path to the file to read.
            metadata: Optional metadata for this knowledge source.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(file_path=file_path, metadata=metadata, **kwargs)

    def get_content(self) -> str:
        """
        Get the content of this knowledge source.

        Returns:
            The content of this knowledge source.
        """
        try:
            import pypdf
        except ImportError:
            raise ImportError(
                "pypdf is required to read PDF files. "
                "Please install it with: pip install pypdf"
            )

        # Read PDF file
        with open(self.file_path, "rb") as f:
            pdf = pypdf.PdfReader(f)
            content = ""
            for page in pdf.pages:
                content += page.extract_text() + "\n\n"

        return content
