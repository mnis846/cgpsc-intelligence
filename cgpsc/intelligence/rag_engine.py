from __future__ import annotations

import logging
import uuid
from typing import Any

from cgpsc.intelligence.embeddings import (
    get_chroma_client,
    get_embedding_function,
    get_or_create_collection,
    query_collection,
)
from cgpsc.intelligence.ollama_client import ensure_model_exists, ollama_chat
from cgpsc.intelligence.personas import get_persona

logger = logging.getLogger("cgpsc.rag_engine")


class RAGEngine:
    """
    Production-grade RAG Engine for CGPSC.

    Features:
    - Real ChromaDB vector search
    - Source citations with relevance scores
    - Persona-aware prompting
    - Conversation history support
    - Metadata filtering
    """

    def __init__(self, persist_directory: str = "./var/vector_db"):
        self.client = get_chroma_client(persist_directory)
        self.collection = get_or_create_collection(self.client)
        self.persist_directory = persist_directory
        logger.info("RAG Engine initialized with ChromaDB")

    def add_pyq_documents(self, questions: list[dict[str, Any]]):
        """Ingest normalized PYQ documents into vector DB."""
        if not questions:
            return

        documents = []
        metadatas = []
        ids = []

        for q in questions:
            text = f"{q.get('question', '')} {' '.join(q.get('options', {}).values())}"
            meta = {
                "year": q.get("year"),
                "subject": q.get("subject"),
                "topic": q.get("topic"),
                "difficulty": q.get("difficulty"),
                "question_no": q.get("question_no"),
            }
            documents.append(text)
            metadatas.append({k: v for k, v in meta.items() if v is not None})
            ids.append(str(uuid.uuid4()))

        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
        logger.info(f"Ingested {len(questions)} PYQs into vector database")

    def retrieve_context(
        self,
        query: str,
        k: int = 6,
        filters: dict | None = None,
    ) -> tuple[str, list[dict]]:
        """Retrieve relevant context + sources."""
        results = query_collection(self.collection, query, n_results=k, where=filters)

        if not results.get("documents") or not results["documents"][0]:
            return "No relevant PYQs found in the database.", []

        docs = results["documents"][0]
        metas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        context_parts = []
        sources = []

        for i, (doc, meta, dist) in enumerate(zip(docs, metas, distances)):
            year = meta.get("year", "?")
            subject = meta.get("subject", "General")
            relevance = round(1 - dist, 3) if dist else 0.8

            context_parts.append(f"[{i+1}] ({year} - {subject}) {doc[:400]}...")

            sources.append(
                {
                    "id": i + 1,
                    "year": year,
                    "subject": subject,
                    "relevance": relevance,
                    "snippet": doc[:200] + "..." if len(doc) > 200 else doc,
                }
            )

        context = "\n\n".join(context_parts)
        return context, sources

    def chat(
        self,
        query: str,
        persona: str = "mentor",
        k: int = 6,
        filters: dict | None = None,
        history: list[dict] | None = None,
        model: str = "llama3.1:8b",
    ) -> dict[str, Any]:
        """Main chat method with RAG + persona."""
        active_persona = get_persona(persona)
        ensure_model_exists(model)

        context, sources = self.retrieve_context(query, k=k, filters=filters)

        # Build conversation history
        history_text = ""
        if history:
            for msg in history[-4:]:  # last 4 messages
                role = msg.get("role", "user")
                content = msg.get("content", "")
                history_text += f"{role.capitalize()}: {content}\n"

        system_prompt = active_persona.build_system_prompt(
            context=context, query=query, history=history_text
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ]

        try:
            resp = ollama_chat(model=model, messages=messages, temperature=0.6, num_predict=700)
            answer = resp.json()["message"]["content"]
        except Exception as e:
            logger.error(f"Ollama chat failed: {e}")
            answer = f"Sorry, I encountered an error: {str(e)}"

        return {
            "answer": answer.strip(),
            "sources": sources,
            "persona": active_persona.name,
            "model_used": model,
        }
