import requests
from ai.base_processor import BaseAIProcessor

class PerplexityProcessor(BaseAIProcessor):
    """Handles processing text using Perplexity API"""
    
    def __init__(self, api_key, model="sonar-pro"):
        super().__init__(f"Perplexity {model}")
        self.api_key = api_key
        self.model = model
    
    def _execute_model_request(self, text):
        """Send extracted text to Perplexity API for MCQ analysis"""
        print(f"Processing text with Perplexity {self.model}...")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an assistant and finance expert that analyzes multiple choice questions and determines the correct answer."
                },
                {
                    "role": "user",
                    "content": f"This image contains a multiple choice question. Using the latest information tell me which answer is correct. Only tell me the correct answer, no explanation needed.\n\n{text}\n\nIMPORTANT OUTPUT FORMATTING INSTRUCTIONS:\n- If the question has multiple choice options (A, B, C, D, etc.), respond with ONLY the letter (e.g., 'A' or 'B')\n- If the question asks for a number, respond with ONLY the number (e.g., '4' not 'four' or '4 times')\n- If the question asks for a time period, respond with the most concise standard form (e.g., 'Quarterly' for questions about reporting frequency)\n- If the question asks for a percentage, respond with ONLY the number and % symbol (e.g., '15%')\n- If the question asks for a dollar amount, respond with ONLY the number and $ symbol (e.g., '$100')\n- Do not include periods, explanatory text, or elaboration\n- Do not include phrases like 'The answer is' or 'The correct answer is'\n- Respond with the most standardized, concise form possible"
                }
            ]
        }
        
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            print(f"Error ({self.model}): {response.status_code}")
            print(response.text)
            return f"Failed to process with {self.model}"
        
        response_data = response.json()
        answer = response_data["choices"][0]["message"]["content"]
        return answer 