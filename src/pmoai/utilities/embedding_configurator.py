import os
from typing import Any, Dict, Optional

from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction


class EmbeddingConfigurator:
    """
    Utility class for configuring embeddings.
    """

    def configure_embedder(
        self, embedder_config: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Configure the embedder based on the provided configuration.

        Args:
            embedder_config: Optional configuration for the embedder.

        Returns:
            The configured embedder.
        """
        if not embedder_config:
            return self._create_default_embedding_function()

        # If a custom embedder is provided, use it
        if "embedder" in embedder_config:
            return embedder_config["embedder"]

        # Otherwise, configure based on the provider
        provider = embedder_config.get("provider", "openai")
        if provider == "openai":
            api_key = embedder_config.get("api_key") or os.getenv("OPENAI_API_KEY")
            model_name = embedder_config.get("model_name", "text-embedding-3-small")
            return OpenAIEmbeddingFunction(api_key=api_key, model_name=model_name)
        else:
            raise ValueError(f"Unsupported embedder provider: {provider}")

    def _create_default_embedding_function(self) -> Any:
        """
        Create a default embedding function using OpenAI.

        Returns:
            The default embedding function.
        """
        return OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-3-small"
        )
