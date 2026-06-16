import logging
import os

from cgpsc.intelligence.ollama_client import ensure_model_exists, ollama_post, OllamaModelNotFoundError
from cgpsc.intelligence.personas import get_persona

logger = logging.getLogger("cgpsc.rag")


class CGPSCRAG:
    def __init__(self, persist_directory: str | None = None):
        self.persist_directory = persist_directory or "./var/vector_db"
        os.makedirs(self.persist_directory, exist_ok=True)
        logger.info("RAG initialized (Ollama mode)")

    def chat(
        self,
        query: str,
        filter_metadata: dict | None = None,
        k: int = 5,
        prefer_notes: bool = True,
        persona: str | None = None,
    ) -> dict:
        active_persona = get_persona(persona)

        # For now we use simple context. In future this will use ChromaDB
        context = "Previous Year Questions and notes related to CGPSC."

        ensure_model_exists("llama3.1:8b")  # Change if you use different model

        system_prompt = active_persona.build_system_prompt(context=context, query=query)

        try:
            resp = ollama_post(
                "/api/chat",
                payload={
                    "model": "llama3.1:8b",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query},
                    ],
                    "stream": False,
                    "options": {"temperature": 0.6, "num_predict": 500},
                },
                caller="rag.chat",
            )
            answer = resp.json()["message"]["content"]
        except Exception as e:
            logger.error(f"Ollama call failed: {e}")
            answer = f"Error calling Ollama: {str(e)}"

        return {
            "answer": answer.strip(),
            "sources": [],
            "persona": active_persona.name,
        }

    def get_stats(self) -> dict:
        return {"total_documents": 0, "mode": "ollama"}
