from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

from cgpsc.shared.paths import PATHS

logger = logging.getLogger(__name__)


class AnalyticsEngine:
    def __init__(self, repository=None):
        self.repository = repository
        self._snapshot = None
        self._last_fingerprint = None

    @staticmethod
    def catalog_fingerprint() -> str:
        """Create a deterministic fingerprint of the current catalog."""
        catalog_dir = PATHS.catalog_questions_dir
        if not catalog_dir.exists():
            return ""
        hasher = hashlib.sha256()
        for json_file in sorted(catalog_dir.glob("*.json")):
            hasher.update(json_file.read_bytes())
        return hasher.hexdigest()

    def is_stale(self) -> bool:
        current = self.catalog_fingerprint()
        return current != self._last_fingerprint

    def compute(self, force: bool = False) -> dict[str, Any]:
        if not force and self._snapshot and not self.is_stale():
            return self._snapshot

        logger.info("AnalyticsEngine computing snapshot...")
        # Placeholder - in real implementation this would load questions and compute stats
        snapshot = {
            "manifest": {
                "years": [2023, 2024, 2025],
                "total_questions": 1250,
                "classified_questions": 1180,
                "catalog_fingerprint": self.catalog_fingerprint(),
            },
            "topic_frequency": {},
            "subject_trends": {},
            "priority_rankings": {},
            "intelligence_report": {},
        }
        self._snapshot = snapshot
        self._last_fingerprint = snapshot["manifest"]["catalog_fingerprint"]
        return snapshot

    def get_snapshot(self, refresh: bool = False) -> dict[str, Any]:
        if refresh or self._snapshot is None:
            return self.compute(force=True)
        return self._snapshot

    def load_normalized_questions(self) -> list[dict[str, Any]]:
        """Load all questions from catalog in normalized format."""
        # This would normally load from data/catalog/questions/*.json
        return []
