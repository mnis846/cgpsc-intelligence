import logging
from cgpsc.intelligence.personas import get_persona

logger = logging.getLogger("cgpsc.rag")


class CGPSCRAG:
    def __init__(self, persist_directory=None):
        self.persist_directory = persist_directory

    def chat(self, query: str, persona: str | None = None, **kwargs):
        active = get_persona(persona)
        # Placeholder response
        return {
            "answer": f"[{active.name}] This is a placeholder answer for: {query}",
            "sources": [],
            "persona": active.name,
        }

    def get_stats(self):
        return {"total_documents": 0}
