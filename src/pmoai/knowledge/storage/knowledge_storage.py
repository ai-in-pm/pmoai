import os
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
from pydantic import BaseModel, ConfigDict

from pmoai.knowledge.embedder.fastembed import FastEmbed
from pmoai.knowledge.storage.base_knowledge_storage import BaseKnowledgeStorage
from pmoai.utilities.paths import db_storage_path


class KnowledgeStorage(BaseKnowledgeStorage, BaseModel):
    """
    Knowledge storage implementation using ChromaDB.

    This class provides a simple vector store implementation for knowledge storage.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(
        self,
        collection_name: Optional[str] = None,
        embedder: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the knowledge storage.

        Args:
            collection_name: Name of the collection to use.
            embedder: Optional embedder configuration.
        """
        self.collection_name = collection_name or f"knowledge_{uuid.uuid4().hex[:8]}"
        self.embedder_config = embedder or {}
        self.embedder = FastEmbed(**self.embedder_config)
        self.client = None
        self.collection = None

    def initialize_knowledge_storage(self) -> None:
        """
        Initialize the knowledge storage.
        """
        try:
            import chromadb
        except ImportError:
            raise ImportError(
                "chromadb is required for knowledge storage. "
                "Please install it with: pip install chromadb"
            )

        # Create the storage directory if it doesn't exist
        storage_dir = os.path.join(db_storage_path(), "chroma")
        os.makedirs(storage_dir, exist_ok=True)

        # Initialize the client
        self.client = chromadb.PersistentClient(path=storage_dir)

        # Get or create the collection
        try:
            self.collection = self.client.get_collection(
                name=self.collection_name,
                embedding_function=None,  # We'll handle embeddings ourselves
            )
        except ValueError:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=None,  # We'll handle embeddings ourselves
            )

    def add_texts(
        self, texts: List[str], metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add texts to the knowledge storage.

        Args:
            texts: List of texts to add.
            metadata: Optional metadata to associate with the texts.
        """
        if not texts:
            return

        if self.collection is None:
            self.initialize_knowledge_storage()

        # Generate embeddings
        embeddings = self.embedder.embed_texts(texts)

        # Generate IDs
        ids = [f"doc_{uuid.uuid4().hex}" for _ in range(len(texts))]

        # Prepare metadata
        metadatas = [metadata or {} for _ in range(len(texts))]

        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=[embedding.tolist() for embedding in embeddings],
            documents=texts,
            metadatas=metadatas,
        )

    def search(
        self,
        query: Union[str, List[str]],
        limit: int = 5,
        score_threshold: float = 0.0,
    ) -> List[Dict[str, Any]]:
        """
        Search for texts in the knowledge storage.

        Args:
            query: Query text or list of query texts.
            limit: Maximum number of results to return.
            score_threshold: Minimum score for a result to be included.

        Returns:
            List of dictionaries containing the search results.
        """
        if self.collection is None:
            self.initialize_knowledge_storage()

        # Handle single query
        if isinstance(query, str):
            query = [query]

        # Generate embeddings
        query_embeddings = self.embedder.embed_texts(query)

        # Search
        results = []
        for i, embedding in enumerate(query_embeddings):
            result = self.collection.query(
                query_embeddings=[embedding.tolist()],
                n_results=limit,
                include=["documents", "metadatas", "distances"],
            )

            # Process results
            for j in range(len(result["ids"][0])):
                distance = result["distances"][0][j]
                # Convert distance to score (1.0 - distance)
                score = 1.0 - distance

                if score >= score_threshold:
                    results.append(
                        {
                            "text": result["documents"][0][j],
                            "metadata": result["metadatas"][0][j],
                            "score": score,
                        }
                    )

        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)

        # Limit results
        return results[:limit]

    def reset(self) -> None:
        """
        Reset the knowledge storage.
        """
        if self.client is not None and self.collection is not None:
            self.client.delete_collection(self.collection_name)
            self.collection = None
            self.initialize_knowledge_storage()
