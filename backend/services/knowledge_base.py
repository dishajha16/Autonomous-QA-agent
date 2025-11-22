import json
import os
from typing import Dict, Any

KNOWLEDGE_FILE = "backend/data/knowledge.json"


def save_knowledge(knowledge: Dict[str, Any]) -> None:
    """
    Save structured knowledge base to knowledge.json.
    """
    os.makedirs(os.path.dirname(KNOWLEDGE_FILE), exist_ok=True)
    with open(KNOWLEDGE_FILE, "w") as f:
        json.dump(knowledge, f, indent=2)


def load_knowledge() -> Dict[str, Any]:
    """
    Load knowledge base from knowledge.json.
    """
    if not os.path.exists(KNOWLEDGE_FILE):
        raise FileNotFoundError(
            "Knowledge base not found. Please run ingestion first."
        )
    with open(KNOWLEDGE_FILE, "r") as f:
        return json.load(f)


def knowledge_summary(knowledge: Dict[str, Any]) -> Dict[str, int]:
    """
    Provides summary counts of knowledge base components.
    """
    return {
        "total_requirements": len(knowledge.get("requirements", [])),
        "total_ui_elements": len(knowledge.get("ui_elements", [])),
    }
