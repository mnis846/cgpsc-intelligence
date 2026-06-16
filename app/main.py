from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import chat, mock, analytics, personas

app = FastAPI(
    title="CGPSC Intelligence API",
    description="Production-grade backend for CGPSC RAG, Analytics & Mock Generation",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api")
app.include_router(mock.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(personas.router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "CGPSC Intelligence API v0.2",
        "status": "running",
        "docs": "/docs",
    }
