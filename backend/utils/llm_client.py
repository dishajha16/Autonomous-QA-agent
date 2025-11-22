import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

class GeminiLLM:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")  # as per your requirement

    def generate(self, prompt: str):
        response = self.model.generate_content(prompt)
        return response.text
