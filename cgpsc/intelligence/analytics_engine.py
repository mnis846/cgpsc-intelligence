from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any

logger = logging.getLogger("cgpsc.analytics")


class AnalyticsEngine:
    """
    Advanced Analytics Engine for CGPSC PYQs.

    Computes:
    - Topic frequency & importance
    - Year-over-year trends
    - Priority rankings (what matters most)
    - Subject-wise breakdowns
    """

    def __init__(self, questions: list[dict[str, Any]] | None = None):
        self.questions = questions or []
        self._snapshot: dict[str, Any] | None = None

    def set_questions(self, questions: list[dict[str, Any]]):
        self.questions = questions
        self._snapshot = None

    def compute(self, force: bool = False) -> dict[str, Any]:
        if self._snapshot and not force:
            return self._snapshot

        if not self.questions:
            return self._empty_snapshot()

        logger.info(f"Computing analytics on {len(self.questions)} questions...")

        subject_freq: dict[str, int] = defaultdict(int)
        topic_freq: dict[str, int] = defaultdict(int)
        year_freq: dict[str, int] = defaultdict(int)
        difficulty_freq: dict[str, int] = defaultdict(int)

        topic_by_year: dict[str, dict[int, int]] = defaultdict(lambda: defaultdict(int))

        for q in self.questions:
            subject = q.get("subject") or q.get("classification", {}).get("primary", {}).get("subject", "Unknown")
            topic = q.get("topic") or "General"
            year = int(q.get("year", 0)) or 0
            difficulty = q.get("difficulty") or "medium"

            subject_freq[subject] += 1
            topic_freq[topic] += 1
            if year > 0:
                year_freq[year] += 1
                topic_by_year[topic][year] += 1
            difficulty_freq[difficulty] += 1

        # Priority score = frequency * recency weight
        priority_rankings = []
        for topic, count in sorted(topic_freq.items(), key=lambda x: -x[1])[:30]:
            years = list(topic_by_year[topic].keys())
            recent_weight = sum(1.5 if y >= 2023 else 1.0 for y in years)
            score = count * recent_weight / max(len(years), 1)
            priority_rankings.append(
                {
                    "topic": topic,
                    "frequency": count,
                    "priority_score": round(score, 2),
                    "years_appeared": sorted(years, reverse=True),
                }
            )

        snapshot = {
            "total_questions": len(self.questions),
            "subject_distribution": dict(sorted(subject_freq.items(), key=lambda x: -x[1])),
            "topic_frequency": dict(sorted(topic_freq.items(), key=lambda x: -x[1])[:25]),
            "year_distribution": dict(sorted(year_freq.items())),
            "difficulty_distribution": dict(difficulty_freq),
            "priority_rankings": priority_rankings,
            "top_overdue_topics": self._find_overdue_topics(topic_by_year),
        }

        self._snapshot = snapshot
        return snapshot

    def _find_overdue_topics(self, topic_by_year: dict) -> list[dict]:
        overdue = []
        for topic, years in topic_by_year.items():
            if not years:
                continue
            last_year = max(years.keys())
            if last_year <= 2022:  # Not appeared recently
                overdue.append(
                    {
                        "topic": topic,
                        "last_appeared": last_year,
                        "frequency": sum(years.values()),
                    }
                )
        return sorted(overdue, key=lambda x: -x["frequency"])[:10]

    def _empty_snapshot(self) -> dict:
        return {
            "total_questions": 0,
            "subject_distribution": {},
            "topic_frequency": {},
            "year_distribution": {},
            "difficulty_distribution": {},
            "priority_rankings": [],
            "top_overdue_topics": [],
        }

    def get_priority_topics(self, limit: int = 15) -> list[dict]:
        snap = self.compute()
        return snap.get("priority_rankings", [])[:limit]
