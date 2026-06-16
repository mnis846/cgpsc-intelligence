from fastapi import APIRouter, Depends
from pydantic import BaseModel

from cgpsc.intelligence.mock_generator import MockGenerator
from cgpsc.intelligence.rag_engine import RAGEngine

router = APIRouter(tags=["Mock Generator"])

_rag_engine = None


def get_rag_engine():
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine()
    return _rag_engine


class MockRequest(BaseModel):
    count: int = 100
    subjects: list[str] | None = None
    year_from: int | None = None
    year_to: int | None = None
    difficulties: list[str] | None = None
    shuffle_options: bool = True


@router.post("/mock/generate")
def generate_mock(req: MockRequest, rag: RAGEngine = Depends(get_rag_engine)):
    # Get questions from the vector database for mock generation
    try:
        # Perform a broad query to get diverse questions
        results = rag.collection.query(
            query_texts=["CGPSC exam question"],
            n_results=min(req.count * 3, 300),  # Get more than needed for filtering
            include=["metadatas", "documents"],
        )

        questions = []
        if results.get("metadatas") and results["metadatas"][0]:
            for i, meta in enumerate(results["metadatas"][0]):
                doc = results["documents"][0][i] if results.get("documents") else ""
                q = {
                    "question": doc,
                    "options": {"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"},
                    "correct_answer": "A",
                    "subject": meta.get("subject", "General"),
                    "topic": meta.get("topic", "General"),
                    "difficulty": meta.get("difficulty", "medium"),
                    "year": meta.get("year", 2020),
                }
                questions.append(q)

        # Use MockGenerator
        generator = MockGenerator(questions)
        paper = generator.generate(
            count=req.count,
            subjects=req.subjects,
            year_from=req.year_from,
            year_to=req.year_to,
            difficulties=req.difficulties,
            shuffle_options=req.shuffle_options,
        )

        return paper.to_dict()

    except Exception as e:
        return {
            "error": str(e),
            "message": "Could not generate mock. Make sure you have ingested PYQ data.",
        }
