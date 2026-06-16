from __future__ import annotations

from abc import ABC, abstractmethod


class BasePersona(ABC):
    name: str
    description: str

    @abstractmethod
    def build_system_prompt(self, *, context: str, query: str) -> str:
        pass


class MentorPersona(BasePersona):
    name = "mentor"
    description = "Clear, analytical CGPSC exam mentor"

    def build_system_prompt(self, *, context: str, query: str) -> str:
        return f"You are a helpful CGPSC mentor.\nContext: {context}\nQuestion: {query}"


class YodaPersona(BasePersona):
    name = "yoda"
    description = "Wise Yoda-style guide"

    def build_system_prompt(self, *, context: str, query: str) -> str:
        return f"Hmm. Context you have: {context}. Question: {query}. Answer you must."


class SocraticPersona(BasePersona):
    name = "socratic"
    description = "Guides through questions"

    def build_system_prompt(self, *, context: str, query: str) -> str:
        return f"Context: {context}\nQuestion: {query}\nWhat do you think?"


PERSONAS = {
    "mentor": MentorPersona(),
    "yoda": YodaPersona(),
    "socratic": SocraticPersona(),
}


def get_persona(name: str | None = None):
    return PERSONAS.get((name or "mentor").lower(), PERSONAS["mentor"])


def list_personas():
    return [{"name": p.name, "description": p.description} for p in PERSONAS.values()]
