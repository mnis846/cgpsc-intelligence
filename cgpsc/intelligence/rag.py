import logging
import os

from cgpsc.intelligence.ollama_client import ensure_model_exists, ollama_post

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

        # Simple context for now (will be replaced with real retrieval later)
        context = "Previous Year Questions and notes related to CGPSC."

        # Use a lighter model to avoid memory issues
        model_name = "llama3.2:3b"
        ensure_model_exists(model_name)

        system_prompt = active_persona.build_system_prompt(context=context, query=query)

        try:
            resp = ollama_post(
                "/api/chat",
                payload={
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query},
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.6,
                        "num_predict": 300,
                        "num_ctx": 2048,   # Reduced context to save memory
                    },
                },
                caller="rag.chat",
            )
            answer = resp.json()["message"]["content"]
        except Exception as e:
            logger.error(f"Ollama call failed: {e}")
            answer = (
                f"Error calling Ollama: {str(e)}. "
                "Try using a lighter model like llama3.2:3b or reduce context size."
            )

        return {
            "answer": answer.strip(),
            "sources": [],
            "persona": active_persona.name,
        }

    def get_stats(self) -> dict:
        return {"total_documents": 0, "mode": "ollama"}
