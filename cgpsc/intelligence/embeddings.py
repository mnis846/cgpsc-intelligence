from __future__ import annotations

import logging
import os
from typing import Any

import chromadb
from chromadb.utils import embedding_functions

logger = logging.getLogger("cgpsc.embeddings")


def get_chroma_client(persist_directory: str = "./var/vector_db") -> chromadb.PersistentClient:
    """Get or create a persistent ChromaDB client."""
    os.makedirs(persist_directory, exist_ok=True)
    return chromadb.PersistentClient(path=persist_directory)


def get_embedding_function(model_name: str = "nomic-embed-text"):
    """Return Ollama embedding function for ChromaDB."""
    return embedding_functions.OllamaEmbeddingFunction(
        model_name=model_name,
        url="http://localhost:11434/api/embeddings",
    )


def get_or_create_collection(
    client: chromadb.PersistentClient,
    name: str = "cgpsc_pyqs",
    embedding_function=None,
):
    """Get or create collection with proper embedding function."""
    if embedding_function is None:
        embedding_function = get_embedding_function()

    try:
        collection = client.get_collection(name=name, embedding_function=embedding_function)
    except Exception:
        collection = client.create_collection(
            name=name,
            embedding_function=embedding_function,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(f"Created new collection: {name}")
    return collection


def add_documents_to_collection(
    collection,
    documents: list[str],
    metadatas: list[dict[str, Any]],
    ids: list[str],
):
    """Add documents with metadata to Chroma collection."""
    if not documents:
        return
    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    logger.info(f"Added {len(documents)} documents to collection")


def query_collection(
    collection,
    query_text: str,
    n_results: int = 6,
    where: dict | None = None,
) -> dict:
    """Query the collection and return results with scores."""
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where=where,
        include=["documents", "metadatas", "distances"],
    )
    return results