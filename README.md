# CGPSC Intelligence Engine v0.2

> **Production-grade local AI system** for CGPSC (Chhattisgarh Public Service Commission) exam preparation.

A powerful, **100% local** intelligence platform featuring:

- **Advanced RAG Chat** with real PYQ grounding + multiple AI personas
- **Analytics Engine** — topic trends, priority rankings, overdue topics
- **Smart Mock Paper Generator**
- **Beautiful Streamlit Frontend** (no coding required)

Everything runs locally using **Ollama** + **ChromaDB**.

---

## Features

| Feature                    | Description                                      | Status      |
|---------------------------|--------------------------------------------------|-------------|
| AI Tutor Chat (RAG)       | Ask questions, get answers grounded in PYQs     | ✅ Working  |
| Multiple Personas         | Mentor, Socratic, Examiner, Storyteller         | ✅ Working  |
| Analytics Dashboard       | Topic frequency, trends, priority scores        | ✅ Working  |
| Smart Mock Generator      | Filter by subject/year/difficulty               | ✅ Working  |
| PYQ Ingestion             | Import from CGPSC Reader format                 | ✅ Working  |
| Source Citations          | See which PYQs were used for answers            | ✅ Working  |

---

## Prerequisites

### 1. Install Ollama

Download and install Ollama from: https://ollama.com

Then pull the required models:

```bash
ollama pull nomic-embed-text      # For embeddings (required)
ollama pull llama3.1:8b           # Recommended chat model
# ollama pull qwen2.5:7b        # Alternative (faster)
```

### 2. Python 3.10+

Make sure you have Python 3.10 or higher installed.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/mnis846/cgpsc-intelligence.git
cd cgpsc-intelligence

# Install the package in editable mode
pip install -e .
```

---

## How to Run

You need **two terminals** running at the same time.

### Terminal 1: Start FastAPI Backend

```bash
uvicorn app.main:app --reload --port 8000
```

### Terminal 2: Start Streamlit Frontend

```bash
streamlit run frontend/streamlit_app.py
```

Then open your browser and go to:

**http://localhost:8501**

---

## Step-by-Step Usage Guide

### 1. Ingest PYQ Data (Important First Step)

The system needs your Previous Year Questions to work properly.

#### Option A: Use your full CGPSC Reader data (Recommended)

```bash
# Copy PYQ files from CGPSC Reader repo
cp /path/to/Cgpsc-reader/data/catalog/questions/*.json data/pyqs/

# Ingest them
python scripts/ingest_pyqs.py --data-dir data/pyqs
```

#### Option B: Use the included sample (for quick testing)

```bash
python scripts/ingest_pyqs.py --sample
```

> **Note**: After ingestion, restart the Streamlit app to see updated analytics.

### 2. Using the Streamlit Interface

Once the app is running, you will see **4 tabs**:

#### Tab 1: AI Tutor Chat
- Choose your preferred **Persona** from the sidebar (Mentor, Socratic, Examiner, Storyteller)
- Type any question related to CGPSC
- The answer will be grounded in real PYQs
- Click on **Sources** to see which questions were used

#### Tab 2: Analytics Dashboard
- Click **"Compute / Refresh Analytics"**
- View:
  - Subject distribution
  - Top priority topics
  - Topics that haven't appeared recently (overdue)

#### Tab 3: Generate Mock Paper
- Set number of questions, subjects, and year range
- Generate smart mock papers

#### Tab 4: PYQ Explorer
- (Coming soon) Search and browse your question bank

---

## Project Structure

```
cgpsc-intelligence/
├── app/                      # FastAPI backend
├── cgpsc/intelligence/     # Core library (RAG, Analytics, Mock)
├── frontend/                 # Streamlit UI
├── data/
│   ├── pyqs/                 # Put your year-wise JSON files here
│   └── sample/               # Sample questions for testing
├── scripts/
│   └── ingest_pyqs.py      # Import PYQs into the system
└── pyproject.toml
```

---

## Configuration

| Setting              | Default                  | How to Change                  |
|----------------------|--------------------------|--------------------------------|
| Chat Model           | `llama3.1:8b`            | Sidebar in Streamlit           |
| Embedding Model      | `nomic-embed-text`       | `cgpsc/intelligence/embeddings.py` |
| Vector DB Location   | `./var/vector_db`        | `RAGEngine(persist_directory=...)` |
| Backend Port         | `8000`                   | `uvicorn ... --port XXXX`      |

---

## Common Issues & Solutions

| Problem                          | Solution                                      |
|----------------------------------|-----------------------------------------------|
| Ollama not running               | Start Ollama desktop app or `ollama serve`    |
| Model not found                  | Run `ollama pull llama3.1:8b`                 |
| ChromaDB metadata error          | Re-run ingestion after latest update          |
| No answers / poor quality        | Ingest more PYQ data + use better model       |
| Port already in use              | Change port: `uvicorn ... --port 8001`        |

---

## Roadmap

- [ ] PDF export for mock papers
- [ ] User progress tracking & weak area detection
- [ ] Better hybrid search (vector + keyword)
- [ ] Docker support
- [ ] Evaluation framework for RAG quality

---

## Related Project

This intelligence engine is designed to work with **[CGPSC Reader](https://github.com/mnis846/Cgpsc-reader)** — the full pipeline + dashboard tool.

---

## License

MIT License

---

**Built for serious CGPSC aspirants who want data-driven, intelligent preparation.**

*Made with speed and quality.*