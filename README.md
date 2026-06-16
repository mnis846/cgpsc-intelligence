# CGPSC Intelligence Engine

> Open-source intelligence layer for CGPSC (Chhattisgarh Public Service Commission) exam preparation.

A modular, local-first intelligence system that turns Previous Year Questions (PYQs) into actionable insights, smart mock papers, and an intelligent chat experience.

---

## Current Phase: Early Development / Foundation Ready

**Status:** Core architecture is in place. The project is **usable for experimentation** but not yet production-ready for end users.

### What Works Right Now

| Component              | Status     | Notes                                      |
|------------------------|------------|--------------------------------------------|
| Analytics Engine       | Partial    | Basic snapshot + fingerprinting            |
| Mock Generator         | Good       | Generates papers with filtering + shuffling|
| Personas System        | Working    | mentor, yoda, socratic                     |
| RAG Chat               | Basic      | Works with Ollama + ChromaDB               |
| API Endpoints          | Partial    | Mock + Chat routes exist                   |

---

## Vision & Benefits (When Completed)

If fully built, this engine can power multiple tools and bring real value to CGPSC aspirants:

### Key Benefits

- **Data-Driven Preparation**
  - See which topics are trending
  - Know which topics are "overdue"
  - Get personalized study priority rankings

- **Smart Mock Papers**
  - Generate high-quality mocks weighted by importance + your weak areas
  - Filter by subject, year, difficulty
  - Option shuffling for better practice

- **Intelligent Chat**
  - Ask questions in natural language
  - Get answers grounded in actual PYQs + your personal notes
  - Choose your preferred teaching style (`mentor`, `yoda`, or `socratic`)

- **Reusable Component**
  - Other developers can integrate this intelligence layer into their own CGPSC apps, websites, or Telegram bots.

---

## Current Limitations & Issues

| Issue                          | Impact                          | Priority |
|--------------------------------|----------------------------------|----------|
| Analytics Engine is incomplete | Many stats are placeholder      | High     |
| No real question catalog      | Mock & RAG need real PYQ data   | High     |
| Heavy dependency on Ollama    | Requires local LLM setup        | Medium   |
| Limited test coverage         | Risk of regressions             | Medium   |
| No proper error handling      | Can break on bad inputs         | Medium   |
| Documentation is early-stage  | Hard for new contributors       | Medium   |

**Biggest blocker right now:** The Analytics Engine needs real implementation of topic frequency, trends, and priority ranking logic.

---

## Architecture Overview

```
cgpsc-intelligence/
├── cgpsc/
│   ├── intelligence/
│   │   ├── analytics_engine.py     # Stats, trends, priority
│   │   ├── mock_generator.py       # Smart mock paper generation
│   │   ├── rag.py                  # RAG + retrieval
│   │   ├── personas.py             # Pluggable teaching styles
│   │   ├── ollama_client.py        # LLM communication
│   │   └── embeddings.py           # Vector embeddings
│   └── api/routes/
│       ├── mock.py
│       └── chat.py
```

---

## Getting Started (for Developers)

### Prerequisites
- Python 3.10+
- Ollama running locally with `nomic-embed-text` and a chat model (e.g. `llama3.1:8b`)

### Installation

```bash
git clone https://github.com/mnis846/cgpsc-intelligence.git
cd cgpsc-intelligence
pip install -e .
```

### Quick Test

```python
from cgpsc.intelligence.mock_generator import MockGenerator

# You need to pass real normalized questions
questions = [...]  # from your catalog
gen = MockGenerator(catalog_questions=questions)
paper = gen.generate(count=50, subjects=["Geography"])
print(paper.title)
```

---

## Roadmap

- [ ] Complete Analytics Engine (frequency, trends, priority)
- [ ] Better integration with real PYQ catalog
- [ ] Improve RAG retrieval quality
- [ ] Add evaluation / testing framework
- [ ] Publish as proper Python package on PyPI
- [ ] Add more personas and fine-tune prompts

---

## How You Can Help

This project is in early stages. Contributions are welcome!

- Improve the Analytics Engine logic
- Add real test cases with sample data
- Better error handling & logging
- Documentation improvements

---

## Related Project

This intelligence engine is used by [CGPSC Reader](https://github.com/mnis846/Cgpsc-reader) — a full pipeline + dashboard tool.

---

## License

MIT License

---

*Built with the goal of making CGPSC preparation more intelligent and data-driven.*
