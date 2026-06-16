import logging
import requests
from requests.exceptions import RequestException, Timeout

logger = logging.getLogger("cgpsc.ollama")

OLLAMA_REQUEST_TIMEOUT = 120


def ollama_post(endpoint: str, payload: dict, timeout: int = OLLAMA_REQUEST_TIMEOUT, caller: str = "unknown"):
    url = f"http://localhost:11434{endpoint}"
    try:
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
        return resp
    except Timeout as e:
        logger.error(f"[{caller}] Ollama timeout: {e}")
        raise
    except RequestException as e:
        logger.error(f"[{caller}] Ollama request failed: {e}")
        raise


def ensure_model_exists(model: str):
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=10)
        models = [m["name"] for m in resp.json().get("models", [])]
        if model not in models:
            logger.warning(f"Model {model} not found. Pulling...")
            requests.post("http://localhost:11434/api/pull", json={"name": model}, timeout=300)
    except Exception as e:
        logger.warning(f"Could not verify model {model}: {e}")


class OllamaModelNotFoundError(Exception):
    def __init__(self, model: str, installed: list):
        self.model = model
        self.installed = installed
        super().__init__(f"Model '{model}' not found in Ollama. Installed: {installed}")
