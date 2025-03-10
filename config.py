import os
from dotenv import load_dotenv
from google.cloud import vision
from google.oauth2 import service_account

class Config:
    """Configuration class for application settings and API credentials"""
    
    def __init__(self):
        load_dotenv()
        
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
        
        self._validate_credentials()
        
        self.vision_client = self._init_vision_client()
    
    def _validate_credentials(self):
        """Validate that required credentials are set"""
        if not self.perplexity_api_key:
            raise ValueError("PERPLEXITY_API_KEY environment variable is not set or empty")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set or empty")
        if not self.google_credentials_path:
            raise ValueError("GOOGLE_CREDENTIALS_PATH environment variable is not set or empty")
    
    def _init_vision_client(self):
        """Initialize and return a Google Vision client"""
        credentials = service_account.Credentials.from_service_account_file(
            self.google_credentials_path
        )
        return vision.ImageAnnotatorClient(credentials=credentials) 