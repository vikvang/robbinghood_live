import time

class BaseAIProcessor:
    """Base class for AI processing"""
    
    def __init__(self, name):
        self.name = name
    
    def process_text(self, text):
        """Process text with the AI model and return the answer"""
        start_time = time.time()
        result = self._execute_model_request(text)
        elapsed_time = time.time() - start_time
        
        return {
            "result": result,
            "time": elapsed_time
        }
    
    def _execute_model_request(self, text):
        """Execute the actual model request - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement _execute_model_request") 