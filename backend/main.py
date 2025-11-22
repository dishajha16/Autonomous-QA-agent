from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from dotenv import load_dotenv

# Import internal services
from backend.services.ingestion import ingest_files
from backend.services.test_case_generator import generate_test_cases
from backend.services.script_generator import generate_scripts
from backend.services.knowledge_base import save_knowledge, load_knowledge, knowledge_summary

# Load environment variables (Gemini API key etc.)
load_dotenv()

# Initialize FastAPI application
app = FastAPI(title="Autonomous QA Agent Backend")

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict later (e.g., ["http://localhost:8501"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────
# 1️⃣ Health Check
# ──────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "message": "Backend is live 🚀"}


# ──────────────────────────────
# 2️⃣ Ingest Docs + HTML
# ──────────────────────────────
@app.post("/ingest")
async def ingest_api(files: List[UploadFile] = File(...)):
    """
    Upload support docs + HTML to build knowledge base.
    """
    try:
        knowledge = await ingest_files(files)
        save_knowledge(knowledge)

        return {
            "status": "success",
            "message": "Knowledge base built successfully!",
            "knowledge_summary": knowledge_summary(knowledge),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion error: {str(e)}")


# ──────────────────────────────
# 3️⃣ Generate Test Cases using Gemini
# ──────────────────────────────
@app.post("/generate-test-cases")
async def generate_test_cases_api():
    """
    Generate grounded test cases using Gemini strictly based on knowledge base.
    """
    try:
        knowledge = load_knowledge()

        test_cases = generate_test_cases(knowledge)

        # Save generated cases
        with open("backend/data/test_cases.json", "w") as f:
            import json
            json.dump(test_cases, f, indent=2)

        return {
            "status": "success",
            "total_test_cases": len(test_cases.get("test_cases", [])),
            "test_cases": test_cases,
        }

    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Knowledge base not found. Please ingest documents first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test case generation error: {str(e)}")


# ──────────────────────────────
# 4️⃣ Generate Selenium Scripts
# ──────────────────────────────
@app.post("/generate-scripts")
async def generate_scripts_api(selected_test_ids: List[str]):
    """
    Given selected test case IDs, generate runnable Selenium Python scripts.
    """
    try:
        # Load knowledge + generated test cases
        knowledge = load_knowledge()

        import json
        with open("backend/data/test_cases.json", "r") as f:
            test_cases = json.load(f)

        scripts = generate_scripts(test_cases, knowledge, selected_test_ids)

        script_path = "backend/data/generated_scripts.py"
        with open(script_path, "w") as f:
            f.write(scripts)

        return {
            "status": "success",
            "message": "Scripts generated successfully",
            "generated_file": script_path,
            "code": scripts,
        }

    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Test cases not found. Please generate them first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Script generation error: {str(e)}")


# ──────────────────────────────
# Launch:
# uvicorn backend.main:app --reload
# ──────────────────────────────
