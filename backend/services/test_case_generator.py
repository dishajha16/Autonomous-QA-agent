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
    """
    Generates grounded test cases using Gemini strictly based on the knowledge base.
    Avoids hallucinations, ensures only valid fields and requirements are referenced.
    """
    prompt = f"""
You are an autonomous QA agent specializing in test planning and Selenium UI automation.

Your task is to generate comprehensive functional test cases STRICTLY based on the provided knowledge base:
⛔ Do NOT assume any feature, field, or button outside what is given.
✔ Only use UI elements and requirements EXACTLY as provided.

---
🔎 KNOWLEDGE BASE TO USE:
{json.dumps(knowledge, indent=2)}
---

🛑 RULES:
1. Test cases MUST reference ONLY:
   • UI elements listed under "ui_elements"  
   • Requirements listed under "requirements"  
2. For used elements, refer by their ID, name or text as shown.
3. Do NOT hallucinate labels, features, or new behaviors.
4. Output MUST be valid JSON with the following structure:

{{
  "test_cases": [
    {{
      "test_id": "TC_001",
      "title": "Short but clear test title",
      "related_requirements": ["R1"], 
      "used_elements": ["emailInput"],  
      "preconditions": ["User must be on the checkout page"],
      "steps": [
        "Enter valid email into the 'emailInput' field",
        "Click on the 'payNowButton'"
      ],
      "expected_result": "Payment succeeds and order placed"
    }}
  ]
}}

🔐 Output JSON only. No additional text, no Markdown formatting.
    """

    try:
        raw_output = llm.generate(prompt)
        test_cases = json.loads(raw_output)

        # Validate references
        test_cases = validate_test_cases(test_cases, knowledge)

        return test_cases

    except json.JSONDecodeError:
        return {
            "error": "⚠ Gemini returned invalid JSON. Try regenerating.",
            "raw_output": raw_output
        }
    except Exception as e:
        return {"error": f"Test generation failed: {str(e)}"}
