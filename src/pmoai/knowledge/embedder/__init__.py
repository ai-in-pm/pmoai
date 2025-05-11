"""Embedder module for PMOAI."""

from pmoai.knowledge.embedder.base_embedder import BaseEmbedder
from pmoai.knowledge.embedder.fastembed import FastEmbed

__all__ = ["BaseEmbedder", "FastEmbed"]
