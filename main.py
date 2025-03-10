import os
from config import Config
from camera.camera_manager import CameraManager
from ocr.ocr_processor import OCRProcessor
from ui.display import DisplayManager
from core.app import RobbinHoodApp

def main():
    """Main entry point for the RobbinHood application"""
    try:
        config = Config()
        
        # get cams 
        available_cameras = CameraManager.list_available_cameras()
        if not available_cameras:
            print("No cameras detected. Ensure your camera is connected and permissions are granted.")
            return
        
        print(f"Detected {len(available_cameras)} camera(s)")
        
        camera_index = 0 # defaults to first cam
        camera_name = None
        # listing out the cameras 
        if len(available_cameras) > 1:
            print("\nAvailable cameras:")
            for i, (idx, name) in enumerate(available_cameras):
                print(f"{i+1}. {name}")
            
            try:
                selection = int(input(f"Select camera (1-{len(available_cameras)}): "))
                if 1 <= selection <= len(available_cameras):
                    camera_index, camera_name = available_cameras[selection-1]
                else:
                    camera_index, camera_name = available_cameras[0]
                    print(f"Invalid selection. Using {camera_name}.")
            except ValueError:
                camera_index, camera_name = available_cameras[0]
                print(f"Invalid input. Using {camera_name}.")
        else:
            camera_index, camera_name = available_cameras[0]
        
        camera_manager = CameraManager(camera_index, camera_name)
        print(f"Using {camera_name}")
        
        ocr_processor = OCRProcessor(config.vision_client)
        display_manager = DisplayManager(camera_manager)
        
        app = RobbinHoodApp(config, camera_manager, ocr_processor, display_manager)
        app.run()
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 