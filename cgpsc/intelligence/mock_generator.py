from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class MockQuestion:
    question_no: int
    question: str
    options: dict[str, str]
    correct_answer: str
    subject: str
    topic: str
    subtopic: str
    difficulty: str
    source_year: int
    original_question_no: int

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class MockPaper:
    title: str
    total_questions: int
    duration_minutes: int
    questions: list[MockQuestion] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "total_questions": len(self.questions),
            "duration_minutes": self.duration_minutes,
            "questions": [q.to_dict() for q in self.questions],
        }


class MockGenerator:
    def __init__(self, catalog_questions: list[dict], priority_rankings: dict | None = None):
        self._questions = catalog_questions
        self._priority = priority_rankings or {}

    def generate(self, count: int = 100, **kwargs) -> MockPaper:
        # Simplified version for open-source release
        selected = self._questions[:count]
        questions = []
        for i, q in enumerate(selected, 1):
            questions.append(MockQuestion(
                question_no=i,
                question=q.get("question", ""),
                options=q.get("options", {}),
                correct_answer=q.get("correct_answer", ""),
                subject=q.get("subject", "General"),
                topic=q.get("topic", ""),
                subtopic=q.get("subtopic", ""),
                difficulty=q.get("difficulty", "medium"),
                source_year=q.get("year", 0),
                original_question_no=q.get("question_no", 0),
            ))
        return MockPaper(title="CGPSC Mock Paper", total_questions=len(questions), duration_minutes=120, questions=questions)

    def available_subjects(self):
        return sorted({q.get("subject") for q in self._questions if q.get("subject")})
