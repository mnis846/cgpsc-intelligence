from __future__ import annotations

from abc import ABC, abstractmethod


class BasePersona(ABC):
    name: str
    description: str

    @abstractmethod
    def build_system_prompt(self, *, context: str, query: str) -> str:
        """Return the full system prompt for this persona."""


class MentorPersona(BasePersona):
    name = "mentor"
    description = "Clear, analytical CGPSC exam mentor — direct and structured."

    def build_system_prompt(self, *, context: str, query: str) -> str:
        return f"""You are an expert CGPSC exam preparation mentor.

Context from knowledge base:
{context}

Guidelines:
- Be direct and analytical.
- Cite years and subjects when relevant.
- Keep answers concise but complete.

User Question: {query}"""


class YodaPersona(BasePersona):
    name = "yoda"
    description = "Wise Yoda-style guide (for fun)."

    def build_system_prompt(self, *, context: str, query: str) -> str:
        return f"""Hmm. You have context: {context}

Question: {query}

Answer you must, young one."""


class SocraticPersona(BasePersona):
    name = "socratic"
    description = "Guides the student through questions."

    def build_system_prompt(self, *, context: str, query: str) -> str:
        return f"""Context: {context}

Student Question: {query}

What do you think? Let's explore together."""


PERSONAS: dict[str, BasePersona] = {
    p.name: p for p in [MentorPersona(), YodaPersona(), SocraticPersona()]
}


def get_persona(name: str | None = None) -> BasePersona:
    key = (name or "mentor").lower().strip()
    return PERSONAS.get(key, PERSONAS["mentor"])


def list_personas() -> list[dict[str, str]]:
    return [{"name": p.name, "description": p.description} for p in PERSONAS.values()]
