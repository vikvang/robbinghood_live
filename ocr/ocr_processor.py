from google.cloud import vision
import os

class OCRProcessor:
    """Handles OCR processing using Google Cloud Vision API"""
    
    def __init__(self, vision_client):
        self.vision_client = vision_client
    
    def extract_text(self, image_path):
        """Extract text from the image using Google Cloud Vision OCR"""
        print("Extracting text with OCR...")
        
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        
        # text detection
        response = self.vision_client.text_detection(image=image)
        texts = response.text_annotations
        
        if len(texts) == 0:
            return "No text detected in the image"
        
        # The first text annotation contains the entire text
        full_text = texts[0].description
        
        if response.error.message:
            print(f"Error: {response.error.message}")
            return None
        
        return full_text 