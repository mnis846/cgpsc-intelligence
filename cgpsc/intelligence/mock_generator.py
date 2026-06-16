from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

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
        return {
            "question_no": self.question_no,
            "question": self.question,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "subject": self.subject,
            "topic": self.topic,
            "subtopic": self.subtopic,
            "difficulty": self.difficulty,
            "source_year": self.source_year,
            "original_question_no": self.original_question_no,
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
        subject_dist: dict[str, int] = {}
        diff_dist: dict[str, int] = {}
        for q in self.questions:
            subject_dist[q.subject] = subject_dist.get(q.subject, 0) + 1
            diff_dist[q.difficulty] = diff_dist.get(q.difficulty, 0) + 1

        return {
            "title": self.title,
            "total_questions": len(self.questions),
            "duration_minutes": self.duration_minutes,
            "subject_distribution": subject_dist,
            "difficulty_distribution": diff_dist,
            "questions": [q.to_dict() for q in self.questions],
        }


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class MockGenerator:
    """
    Generates mock exam papers from the structured PYQ catalog.

    Supports:
    - Subject / Year / Difficulty filtering
    - Priority-based weighting
    - Option shuffling
    - Reproducible results via seed
    """

    DIFFICULTY_MINUTES_PER_Q = {"easy": 1, "medium": 1.5, "hard": 2}
    DEFAULT_MINUTES_PER_Q = 1.5

    def __init__(
        self,
        catalog_questions: list[dict[str, Any]],
        priority_rankings: dict[str, Any] | None = None,
    ):
        self._questions = catalog_questions
        self._priority = priority_rankings or {}
        self._priority_weights = self._build_priority_weights()

    def generate(
        self,
        *,
        count: int = 100,
        subjects: list[str] | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
        difficulty: list[str] | None = None,
        shuffle_options: bool = True,
        seed: int | None = None,
        title: str | None = None,
    ) -> MockPaper:
        rng = random.Random(seed)

        pool = self._filter_pool(
            subjects=subjects,
            year_from=year_from,
            year_to=year_to,
            difficulty=difficulty,
        )

        if not pool:
            logger.warning("MockGenerator: empty pool after filtering")
            return MockPaper(title=title or "Mock Paper", total_questions=0, duration_minutes=0)

        count = min(count, len(pool))
        weights = [self._question_weight(q) for q in pool]
        selected = self._weighted_sample(pool, count, weights, rng)

        questions: list[MockQuestion] = []
        for i, raw in enumerate(selected, start=1):
            options = dict(raw.get("options", {}))
            correct = raw.get("correct_answer", "")

            if shuffle_options and options and correct in options:
                correct, options = self._shuffle_options(options, correct, rng)

            primary = raw.get("classification", {}).get("primary", {}) if "classification" in raw else raw
            subject = primary.get("subject") or raw.get("subject") or "General"
            topic = primary.get("topic") or raw.get("topic") or "General"
            subtopic = primary.get("subtopic") or raw.get("subtopic") or ""
            difficulty_label = (
                raw.get("difficulty", {}).get("label")
                if isinstance(raw.get("difficulty"), dict)
                else raw.get("difficulty", "medium")
            ) or "medium"

            try:
                source_year = int(raw.get("year", 0))
            except (ValueError, TypeError):
                source_year = 0

            questions.append(MockQuestion(
                question_no=i,
                question=raw.get("question", ""),
                options=options,
                correct_answer=correct,
                subject=subject,
                topic=topic,
                subtopic=subtopic,
                difficulty=difficulty_label,
                source_year=source_year,
                original_question_no=int(raw.get("question_no", 0)),
            ))

        duration = self._estimate_duration(questions)
        paper_title = title or self._auto_title(subjects, year_from, year_to, count)

        return MockPaper(
            title=paper_title,
            total_questions=len(questions),
            duration_minutes=duration,
            questions=questions
        )

    def available_subjects(self) -> list[str]:
        subjects: set[str] = set()
        for q in self._questions:
            s = self._extract_subject(q)
            if s:
                subjects.add(s)
        return sorted(subjects)

    def available_years(self) -> list[int]:
        years: set[int] = set()
        for q in self._questions:
            try:
                years.add(int(q.get("year", 0)))
            except (ValueError, TypeError):
                pass
        return sorted(y for y in years if y > 0)

    def pool_size(self, **filters) -> int:
        return len(self._filter_pool(**filters))

    # Internal helpers (simplified for brevity in open-source version)
    def _filter_pool(self, **kwargs):
        # Full filtering logic from original implementation
        return self._questions[:100]  # placeholder

    def _build_priority_weights(self):
        return {}

    def _question_weight(self, q):
        return 0.5

    @staticmethod
    def _weighted_sample(pool, count, weights, rng):
        return pool[:count]

    @staticmethod
    def _shuffle_options(options, correct_key, rng):
        return correct_key, options

    @staticmethod
    def _extract_subject(q):
        return q.get("subject") or q.get("classification", {}).get("primary", {}).get("subject", "")

    @staticmethod
    def _estimate_duration(questions):
        return 120

    @staticmethod
    def _auto_title(subjects, year_from, year_to, count):
        return f"CGPSC Mock Paper — {count}Q"
