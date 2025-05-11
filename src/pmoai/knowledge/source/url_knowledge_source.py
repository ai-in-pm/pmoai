from typing import Any, Dict, Optional

from pydantic import Field

from pmoai.knowledge.source.base_knowledge_source import BaseKnowledgeSource


class URLKnowledgeSource(BaseKnowledgeSource):
    """
    A knowledge source that reads from a URL.
    """

    url: str = Field(..., description="The URL to read")

    def __init__(
        self,
        url: str,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        Initialize a URL knowledge source.

        Args:
            url: The URL to read.
            metadata: Optional metadata for this knowledge source.
            **kwargs: Additional keyword arguments.
        """
        if metadata is None:
            metadata = {}

        # Add URL metadata
        metadata.update(
            {
                "source": url,
                "type": "url",
            }
        )

        super().__init__(url=url, metadata=metadata, **kwargs)

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
        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            raise ImportError(
                "requests and beautifulsoup4 are required to read URLs. "
                "Please install them with: pip install requests beautifulsoup4"
            )

        # Fetch the URL
        response = requests.get(self.url)
        response.raise_for_status()

        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the text
        return soup.get_text()
