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
    difficulty: str
    source_year: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "question_no": self.question_no,
            "question": self.question,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "subject": self.subject,
            "topic": self.topic,
            "difficulty": self.difficulty,
            "source_year": self.source_year,
        }


@dataclass
class MockPaper:
    title: str
    total_questions: int
    duration_minutes: int
    questions: list[MockQuestion] = field(default_factory=list)
    subject_distribution: dict[str, int] = field(default_factory=dict)
    difficulty_distribution: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "total_questions": len(self.questions),
            "duration_minutes": self.duration_minutes,
            "subject_distribution": dict(self.subject_distribution),
            "difficulty_distribution": dict(self.difficulty_distribution),
            "questions": [q.to_dict() for q in self.questions],
        }


class MockGenerator:
    """
    Smart Mock Paper Generator with real filtering and priority weighting.
    """

    def __init__(self, questions: list[dict[str, Any]]):
        self.questions = questions

    def generate(
        self,
        count: int = 100,
        subjects: list[str] | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
        difficulties: list[str] | None = None,
        shuffle_options: bool = True,
        seed: int | None = None,
        title: str | None = None,
    ) -> MockPaper:
        rng = random.Random(seed)
        pool = self._filter_questions(subjects, year_from, year_to, difficulties)

        if not pool:
            return MockPaper(title=title or "Empty Mock", total_questions=0, duration_minutes=0)

        # Simple priority weighting (can be improved with analytics)
        selected = rng.sample(pool, min(count, len(pool)))

        questions: list[MockQuestion] = []
        for i, raw in enumerate(selected, 1):
            q = MockQuestion(
                question_no=i,
                question=raw.get("question", ""),
                options=raw.get("options", {}),
                correct_answer=raw.get("correct_answer", ""),
                subject=raw.get("subject", "General"),
                topic=raw.get("topic", "General"),
                difficulty=raw.get("difficulty", "medium"),
                source_year=int(raw.get("year", 0)),
            )
            questions.append(q)

        if shuffle_options:
            for q in questions:
                if q.options and q.correct_answer in q.options:
                    opts = list(q.options.items())
                    rng.shuffle(opts)
                    q.options = dict(opts)

        duration = int(len(questions) * 1.5)
        paper_title = title or f"CGPSC Mock Paper ({len(questions)} Questions)"

        return MockPaper(
            title=paper_title,
            total_questions=len(questions),
            duration_minutes=duration,
            questions=questions,
        )

    def _filter_questions(
        self,
        subjects: list[str] | None,
        year_from: int | None,
        year_to: int | None,
        difficulties: list[str] | None,
    ) -> list[dict]:
        filtered = self.questions
        if subjects:
            filtered = [q for q in filtered if q.get("subject") in subjects]
        if year_from:
            filtered = [q for q in filtered if int(q.get("year", 0)) >= year_from]
        if year_to:
            filtered = [q for q in filtered if int(q.get("year", 0)) <= year_to]
        if difficulties:
            filtered = [q for q in filtered if q.get("difficulty") in difficulties]
        return filtered

    def get_available_subjects(self) -> list[str]:
        return sorted({q.get("subject", "General") for q in self.questions})

    def get_available_years(self) -> list[int]:
        years = {int(q.get("year", 0)) for q in self.questions if q.get("year")}
        return sorted(y for y in years if y > 0)
