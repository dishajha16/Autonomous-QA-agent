import json
from backend.utils.llm_client import GeminiLLM

llm = GeminiLLM()

def validate_test_cases(test_cases: dict, knowledge: dict):
    """
    Validates that used_elements in each test case actually map to known UI elements from ingestion.
    """
    valid_elements = {
        elem.get("id") or elem.get("name") or elem.get("text")
        for elem in knowledge.get("ui_elements", [])
    }

    for tc in test_cases.get("test_cases", []):
        invalid = set(tc.get("used_elements", [])) - valid_elements
        if invalid:
            tc["validation_warning"] = f"⚠ Invalid elements referenced: {list(invalid)}"

    return test_cases


def generate_test_cases(knowledge: dict) -> dict:
    prompt = f"""
You are an autonomous QA agent specializing in test planning and Selenium UI automation.

Your task is to generate **valid JSON test cases STRICTLY based on the provided knowledge base**.

🚨 CRITICAL RULES 🚨
- Only use UI elements from "ui_elements".
- Only reference requirements from "requirements".
- Do ❌ NOT hallucinate any features or extra fields.
- Do ❌ NOT wrap output in ```json or markdown or add explanations.
- Do only return **valid JSON** exactly in format shown below.

Example format (MUST FOLLOW):

{{
  "test_cases": [
    {{
      "test_id": "TC_001",
      "title": "Short but clear test title",
      "related_requirements": ["R1"],
      "used_elements": ["emailInput"],
      "preconditions": ["User must be on the checkout page"],
      "steps": ["Enter email", "Click pay button"],
      "expected_result": "Payment succeeds"
    }}
  ]
}}

📌 Return ONLY this JSON format. NOTHING else before or after.
📌 No markdown formatting, no triple backticks.

Knowledge Base:
{json.dumps(knowledge, indent=2)}
"""

    try:
        raw_output = llm.generate(prompt).strip()

        # Remove markdown or code fencing if any (safely)
        if raw_output.startswith("```"):
            raw_output = raw_output.replace("```json", "").replace("```", "").strip()

        # Try to parse JSON
        test_cases = json.loads(raw_output)

        # Validate UI element references
        test_cases = validate_test_cases(test_cases, knowledge)

        return test_cases

    except json.JSONDecodeError:
        return {
            "error": "⚠ Gemini returned invalid JSON. Try regenerating.",
            "raw_output": raw_output
        }
    except Exception as e:
        return {"error": f"Test generation failed: {str(e)}"}
