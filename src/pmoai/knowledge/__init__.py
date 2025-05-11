"""Knowledge module for PMOAI."""

from pmoai.knowledge.embedder import BaseEmbedder, FastEmbed
from pmoai.knowledge.knowledge import Knowledge
from pmoai.knowledge.knowledge_config import KnowledgeConfig
from pmoai.knowledge.source import (
    BaseFileKnowledgeSource,
    BaseKnowledgeSource,
    CrewDoclingSource,
    CSVKnowledgeSource,
    ExcelKnowledgeSource,
    FileKnowledgeSource,
    JSONKnowledgeSource,
    PDFKnowledgeSource,
    PMMethodologyKnowledgeSource,
    StringKnowledgeSource,
    TextFileKnowledgeSource,
    URLKnowledgeSource,
)
from pmoai.knowledge.storage import BaseKnowledgeStorage, KnowledgeStorage
from pmoai.knowledge.utils import split_text_into_chunks

__all__ = [
    # Main classes
    "Knowledge",
    "KnowledgeConfig",

    # Embedders
    "BaseEmbedder",
    "FastEmbed",

    # Knowledge sources
    "BaseKnowledgeSource",
    "BaseFileKnowledgeSource",
    "CrewDoclingSource",
    "CSVKnowledgeSource",
    "ExcelKnowledgeSource",
    "FileKnowledgeSource",
    "JSONKnowledgeSource",
    "PDFKnowledgeSource",
    "PMMethodologyKnowledgeSource",
    "StringKnowledgeSource",
    "TextFileKnowledgeSource",
    "URLKnowledgeSource",

    # Storage
    "BaseKnowledgeStorage",
    "KnowledgeStorage",

    # Utilities
    "split_text_into_chunks",
]
