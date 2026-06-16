# CGPSC Intelligence Engine

Open-source intelligence layer for CGPSC (Chhattisgarh Public Service Commission) exam preparation tools.

## Features

- **Analytics Engine**: Topic frequency, trends, priority rankings, pattern intelligence from PYQs
- **Mock Generator**: Statistically weighted mock papers with difficulty, subject, and year filtering + option shuffling
- **RAG Chat**: Retrieval-Augmented Generation with support for user notes
- **Pluggable Personas**: `mentor` (default), `yoda`, `socratic`
- **Fully Local**: Runs with Ollama + ChromaDB

## Installation

```bash
pip install cgpsc-intelligence
```

Or clone and install in editable mode:

```bash
pip install -e .
```

## Quick Usage

```python
from cgpsc.intelligence.analytics_engine import AnalyticsEngine
from cgpsc.intelligence.mock_generator import MockGenerator

# Load analytics
engine = AnalyticsEngine()
snapshot = engine.get_snapshot()

# Generate a mock paper
mock_gen = MockGenerator(catalog_questions=...)
paper = mock_gen.generate(count=100, subjects=["Geography"], difficulty=["easy", "medium"])
```

## Components

- `analytics_engine.py` — Core statistical analysis
- `mock_generator.py` — Intelligent mock paper creation
- `rag.py` — RAG chat engine
- `personas.py` — Pluggable system prompts
- `ollama_client.py` + `embeddings.py` — LLM integration

## Related Projects

This intelligence engine powers [cgpsc-reader](https://github.com/mnis846/Cgpsc-reader).

## License
MIT (or your preferred license)
