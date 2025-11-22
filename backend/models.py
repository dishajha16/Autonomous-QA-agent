from pydantic import BaseModel
from typing import List, Optional, Dict, Any


# ───────────────────────────────────────────────
# 1️⃣ Basic API Models
# ───────────────────────────────────────────────
class HealthResponse(BaseModel):
    status: str
    message: str


# ───────────────────────────────────────────────
# 2️⃣ Ingestion / Knowledge Base Models
# ───────────────────────────────────────────────
class UIElement(BaseModel):
    tag: Optional[str]
    id: Optional[str]
    name: Optional[str]
    type: Optional[str]
    text: Optional[str]
    class_: Optional[str] = None  # "class" is reserved in Python


class KnowledgeBase(BaseModel):
    requirements: List[str]  # Just text chunks from documents
    ui_elements: List[UIElement]


class IngestionResponse(BaseModel):
    status: str
    message: str
    knowledge_summary: Dict[str, int]


# ───────────────────────────────────────────────
# 3️⃣ Test Case Generation Models
# ───────────────────────────────────────────────
class TestCase(BaseModel):
    test_id: str
    title: str
    related_requirements: List[str]
    used_elements: List[str]
    preconditions: List[str]
    steps: List[str]
    expected_result: str


class TestCaseGenerationResponse(BaseModel):
    status: str
    total_test_cases: int
    test_cases: Dict[str, Any]  # since Gemini outputs as JSON dict


# ───────────────────────────────────────────────
# 4️⃣ Script Generation Models
# ───────────────────────────────────────────────
class ScriptGenerationRequest(BaseModel):
    selected_test_ids: List[str]


class ScriptGenerationResponse(BaseModel):
    status: str
    message: str
    generated_file: str
    code: str


# ───────────────────────────────────────────────
# 🎯 Notes
# - Replace Dict[str, Any] with List[TestCase] if Gemini always returns structured TestCase.
# - UIElement.class_: The underscore avoids keyword conflict.
# - These models ensure valid data flow across all APIs.
# ───────────────────────────────────────────────
