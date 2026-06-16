#!/usr/bin/env python3
"""
Ingest PYQ data from CGPSC Reader format into the Intelligence Engine.

Usage:
    python scripts/ingest_pyqs.py --data-dir data/pyqs
    python scripts/ingest_pyqs.py --sample   # Use built-in small sample
"""

import argparse
import json
import logging
from pathlib import Path

from cgpsc.intelligence.rag_engine import RAGEngine
from cgpsc.intelligence.analytics_engine import AnalyticsEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_questions_from_dir(data_dir: Path) -> list[dict]:
    questions = []
    for json_file in sorted(data_dir.glob("*.json")):
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)
            year_questions = data.get("questions", [])
            for q in year_questions:
                q["year"] = data.get("year", q.get("year"))
            questions.extend(year_questions)
    logger.info(f"Loaded {len(questions)} questions from {data_dir}")
    return questions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/pyqs"))
    parser.add_argument("--sample", action="store_true", help="Use built-in sample instead")
    args = parser.parse_args()

    if args.sample:
        # TODO: Load from data/sample/sample_questions.json
        logger.info("Sample mode not fully implemented yet. Using empty.")
        questions = []
    else:
        questions = load_questions_from_dir(args.data_dir)

    if not questions:
        logger.warning("No questions loaded. Exiting.")
        return

    # Ingest into RAG
    rag = RAGEngine()
    rag.add_pyq_documents(questions)
    logger.info("PYQs ingested into ChromaDB for RAG")

    # Prepare Analytics
    analytics = AnalyticsEngine(questions)
    snapshot = analytics.compute(force=True)
    logger.info(f"Analytics computed: {snapshot['total_questions']} questions")
    logger.info("Top priority topics:")
    for item in snapshot.get("priority_rankings", [])[:5]:
        logger.info(f"  - {item['topic']}: {item['priority_score']}")

    logger.info("Ingestion complete!")


if __name__ == "__main__":
    main()
