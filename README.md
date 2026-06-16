# CGPSC Intelligence Engine v0.2

> **Production-ready local intelligence system** for CGPSC aspirants.

A high-performance, local-first platform combining **Advanced RAG**, **Analytics Engine**, **Smart Mock Generator**, and **Pluggable AI Tutors** — all accessible through a beautiful **Streamlit frontend** + **FastAPI backend**.

---

## What's New in v0.2 (Major Upgrade)

- **Full FastAPI Backend** with clean routers and Pydantic models
- **Advanced RAG Engine** with real ChromaDB + embeddings + source citations
- **Powerful Analytics Engine** — topic frequency, trends, priority rankings
- **Beautiful Streamlit Frontend** (no more terminal!)
- **Improved Personas** and system prompts
- **Production-grade code quality** (type hints, error handling, logging)

---

## Architecture

```
CGPSC Intelligence
├── FastAPI Backend (app/)
│   ├── /chat          → AI Tutor (RAG-powered)
│   ├── /mock          → Smart Mock Generator
│   ├── /analytics     → PYQ Analysis + Trends
│   └── /personas      → Available teaching styles
├── Streamlit Frontend (frontend/)
│   ├── Chat with AI Tutor
│   ├── Analytics Dashboard
│   ├── Mock Paper Generator
│   └── PYQ Explorer
├── Core Intelligence (cgpsc/intelligence/)
│   ├── rag_engine.py        → ChromaDB + Ollama RAG
│   ├── analytics_engine.py  → Real statistics & trends
│   ├── mock_generator.py    → Weighted, filtered mocks
│   ├── personas.py          → Mentor, Socratic, Examiner...
│   └── embeddings.py        → Vector embeddings
└── Local LLMs via Ollama
```

---

## Quick Start (Recommended)

### 1. Prerequisites
```bash
# Install Ollama and pull models
ollama pull nomic-embed-text
ollama pull llama3.1:8b          # or qwen2.5:7b, llama3.2:3b
```

### 2. Install
```bash
git clone https://github.com/mnis846/cgpsc-intelligence.git
cd cgpsc-intelligence
pip install -e .
```

### 3. Run Everything
```bash
# Terminal 1: Start FastAPI backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Start beautiful Streamlit frontend
streamlit run frontend/streamlit_app.py
```

Then open **http://localhost:8501** in your browser.

---

## Features

### 1. AI Tutor Chat (RAG-powered)
- Choose from multiple personas (Mentor, Socratic, Strict Examiner, etc.)
- Answers grounded in your PYQ database
- Shows sources with relevance scores
- Conversation history

### 2. Analytics Dashboard
- Topic frequency & importance
- Year-over-year trends
- Overdue / high-priority topics
- Subject-wise breakdowns

### 3. Smart Mock Generator
- Filter by subject, year, difficulty
- Priority-weighted selection
- Option shuffling
- Download as PDF/JSON

### 4. Extensible
- Drop your own normalized PYQ JSON files
- Easy to integrate into other apps

---

## Project Structure

See the architecture diagram above.

---

## Roadmap (Next)
- [ ] Persistent user profiles & weak area tracking
- [ ] PDF export for mock papers
- [ ] Better hybrid search (BM25 + vector)
- [ ] Evaluation harness for RAG quality
- [ ] Docker support

---

**Built for serious CGPSC aspirants who want data-driven, intelligent preparation.**

MIT License
