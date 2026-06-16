# PYQ Data for CGPSC Intelligence

This folder is for normalized CGPSC Previous Year Questions (PYQs).

## Recommended Structure

```
data/
├── pyqs/
│   ├── 2019.json
│   ├── 2020.json
│   ├── ...
│   └── 2025.json
└── sample/
    └── sample_questions.json   # Small subset for testing
```

## Data Format

The project expects data in the same format as the **CGPSC Reader** repo (`mnis846/Cgpsc-reader`):

- `data/catalog/questions/YYYY.json`
- Each file contains `questions[]` array with fields like:
  - `question_no`
  - `question`
  - `options`
  - `classification.primary.subject`
  - `classification.primary.topic`
  - `difficulty.label`
  - `year`

## How to Use

1. Copy your PYQ JSON files from CGPSC Reader into `data/pyqs/`
2. Run the ingestion script:
   ```bash
   python scripts/ingest_pyqs.py
   ```
3. This will populate ChromaDB for RAG and prepare data for Analytics + Mock Generator.

You can also pass questions directly via API or in the Streamlit app.
