def generate_scripts(test_cases: dict, knowledge: dict, selected_test_ids: list[str]) -> str:
    import os  # Needed for path resolution

    ui_elements = knowledge.get("ui_elements", [])
    all_cases = test_cases.get("test_cases", [])
    selected_cases = [tc for tc in all_cases if tc.get("test_id") in selected_test_ids]

    input_mapping = {
        "emailInput": "test@example.com",
        "nameInput": "John Doe",
        "cardNumber": "1234567890123456",
        "expiryDate": "2025-12",
        "cvvInput": "123",
    }

    script = """import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

class TestCheckout(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        html_path = os.path.abspath("backend/data/checkout.html")
        self.driver.get(f"file:///{html_path}")

    def tearDown(self):
        self.driver.quit()
"""

    def resolve_selector(element):
        for ui in ui_elements:
            if element == ui.get("id"):
                return "By.ID", ui.get("id")
            if element == ui.get("name"):
                return "By.NAME", ui.get("name")
            if element == ui.get("text"):
                return "By.XPATH", f"//*[text()='{ui.get('text')}']"
        return None, None

    for tc in selected_cases:
        method_name = f"test_{tc.get('test_id').lower()}"
        script += f"    def {method_name}(self):\n"
        script += f"        print('Executing {tc.get('title')}')\n"
        script += "        driver = self.driver\n\n"

        for element in tc.get("used_elements", []):
            selector, value = resolve_selector(element)
            if not selector:
                script += f"        # ⚠ Could not resolve element: {element}\n"
                continue

            if "button" in element.lower() or "payNow" in element:
                script += f"        driver.find_element({selector}, '{value}').click()\n"
            else:
                test_data = input_mapping.get(element, "test_data")
                script += f"        driver.find_element({selector}, '{value}').send_keys('{test_data}')\n"

        script += "\n        time.sleep(2)\n"
        script += "        # Example assertion:\n"
        script += "        # self.assertIn('Payment Successful', driver.page_source)\n\n"

    script += """
if __name__ == '__main__':
    unittest.main()
"""
    return script
