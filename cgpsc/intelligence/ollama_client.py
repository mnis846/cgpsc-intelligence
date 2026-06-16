from __future__ import annotations

import logging
import requests

from requests.exceptions import RequestException

logger = logging.getLogger("cgpsc.ollama")

OLLAMA_BASE_URL = "http://localhost:11434"


def ensure_model_exists(model_name: str) -> bool:
    """Check if model exists in Ollama, pull if missing."""
    try:
        resp = requests.post(f"{OLLAMA_BASE_URL}/api/show", json={"name": model_name}, timeout=10)
        if resp.status_code == 200:
            return True
        # Try to pull
        logger.info(f"Pulling model {model_name}...")
        requests.post(f"{OLLAMA_BASE_URL}/api/pull", json={"name": model_name}, timeout=300)
        return True
    except RequestException as e:
        logger.error(f"Ollama connection failed: {e}")
        return False


def ollama_chat(
    model: str,
    messages: list[dict],
    temperature: float = 0.7,
    num_predict: int = 512,
    stream: bool = False,
):
    """Make a chat request to Ollama."""
    payload = {
        "model": model,
        "messages": messages,
        "stream": stream,
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
            "num_ctx": 8192,
        },
    }
    resp = requests.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload, timeout=120)
    resp.raise_for_status()
    return resp


def ollama_embed(text: str, model: str = "nomic-embed-text") -> list[float]:
    """Get embedding for a single text."""
    resp = requests.post(
        f"{OLLAMA_BASE_URL}/api/embeddings",
        json={"model": model, "prompt": text},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["embedding"]
