import requests
from ai.base_processor import BaseAIProcessor

class GPT4Processor(BaseAIProcessor):
    """Handles processing text using OpenAI's GPT-4"""
    
    def __init__(self, api_key, model="gpt-4-turbo"):
        super().__init__("GPT-4 Turbo")
        self.api_key = api_key
        self.model = model
    
    def _execute_model_request(self, text):
        """Send text to OpenAI's GPT-4-Turbo for MCQ analysis"""
        print("Processing text with GPT-4-Turbo...")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an assistant and financial expert that analyzes multiple choice questions and determines the correct answer."
                },
                {
                    "role": "user",
                    "content": f"This contains a multiple choice question. Tell me which answer is correct. Only tell me the correct answer, no explanation needed.\n\n{text}"
                }
            ],
            "max_tokens": 100
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            print(f"Error (GPT-4): {response.status_code}")
            print(response.text)
            return "Failed to process with GPT-4"
        
        response_data = response.json()
        answer = response_data["choices"][0]["message"]["content"]
        return answer 