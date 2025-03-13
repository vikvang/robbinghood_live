from google import genai
from google.genai import types
from ai.base_processor import BaseAIProcessor

class GeminiProcessor(BaseAIProcessor):
    """Handles processing text using Google Gemini API with Google Search grounding"""
    
    def __init__(self, api_key, model="gemini-2.0-flash"):
        super().__init__(f"Gemini {model}")
        self.api_key = api_key
        self.model = model
        
        # Configure the Google Gemini client
        self.client = genai.Client(api_key=api_key)
        
    def _execute_model_request(self, text):
        """Send extracted text to Google Gemini API for MCQ analysis with Google Search grounding"""
        print(f"Processing text with Gemini {self.model} using Google Search grounding...")
        
        try:
            # Create a prompt that incorporates the system instructions and the text to analyze
            prompt = f"""You are an assistant and finance expert that analyzes multiple choice questions and determines the correct answer.
            
            This image contains a multiple choice question. Using the latest accurate information from search results, tell me which answer is correct. Only tell me the correct answer letter (A, B, C, D, etc.), no explanation needed.
            
            Question: {text}"""
            
            # Send the request with Google Search grounding enabled
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,  # Low temperature for focused, accurate responses
                    tools=[types.Tool(
                        google_search=types.GoogleSearchRetrieval()
                    )]
                )
            )
            
            # Extract the answer
            answer = response.text.strip() if hasattr(response, 'text') else response.candidates[0].content.parts[0].text
            
            # Ensure the answer is just the letter
            if len(answer) > 5:  # If we got more than just a letter and possibly a period
                # Try to extract just the letter answer
                for line in answer.split('\n'):
                    if len(line.strip()) <= 3 and any(letter in line.upper() for letter in "ABCDE"):
                        return line.strip()
            
            return answer
            
        except Exception as e:
            print(f"Error ({self.model}): {str(e)}")
            return f"Failed to process with {self.model}: {str(e)}"