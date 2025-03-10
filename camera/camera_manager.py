import cv2
import time
import os
import platform
import re

class CameraManager:
    """Manages camera operations like listing, capturing, and displaying video feed"""
    
    @staticmethod
    def list_available_cameras():
        """List all available camera devices with names if possible"""
        available_cameras = []
        camera_names = {}
        
        system = platform.system()
        
        for i in range(10):  # Check first 10 indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    # Get camera name if possible
                    name = None
                    # Try to get camera info from OpenCV
                    backend_name = cap.getBackendName() if hasattr(cap, 'getBackendName') else "Unknown"
                    
                    # These are not guaranteed to work on all platforms/cameras
                    if hasattr(cap, 'get'):
                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        
                        # Try to get more camera info on different platforms
                        if system == "Darwin":  # macOS
                            name = f"Camera {i} ({width}x{height}, {backend_name})"
                            
                            # If it's camera 1 and camera 0 exists, it might be external
                            if i == 1 and 0 in [x[0] for x in available_cameras]:
                                name = f"External Camera ({width}x{height})"
                                
                        elif system == "Windows":
                            name = f"Camera {i} ({width}x{height}, {backend_name})"
                            
                            # Guess if it's a built-in or external camera
                            if i == 0:
                                name = f"Primary Camera ({width}x{height})"
                            elif i == 1:
                                name = f"Secondary Camera ({width}x{height})"
                                
                        elif system == "Linux":
                            name = f"Camera {i} ({width}x{height}, {backend_name})"
                            
                            # On Linux, try to get a better name from device info
                            try:
                                if os.path.exists(f"/dev/video{i}"):
                                    name = f"/dev/video{i} ({width}x{height})"
                            except:
                                pass
                    
                    # Default name if we couldn't determine a better one
                    if name is None:
                        name = f"Camera {i}"
                    
                    available_cameras.append((i, name))
                cap.release()
        
        return available_cameras
    
    def __init__(self, camera_index=0, camera_name=None):
        self.camera_index = camera_index
        self.camera_name = camera_name if camera_name else f"Camera {camera_index}"
        self.cap = None
    
    def open(self):
        """Open the camera"""
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera with index {self.camera_index}")
        # Wait a moment for the camera to initialize
        time.sleep(1)
        return self.cap
    
    def release(self):
        """Release camera resources"""
        if self.cap and self.cap.isOpened():
            self.cap.release()
            cv2.destroyAllWindows()
    
    def capture_image(self, temp_filename="temp_capture.jpg"):
        """Capture an image from the webcam interactively"""
        print(f"Opening {self.camera_name}...")
        
        if not self.cap or not self.cap.isOpened():
            self.open()
        
        print("Camera opened. Press SPACE to capture or ESC to cancel...")
        
        # Show video feed until user presses space to capture
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame")
                break

            cv2.imshow('Capture MCQ (Press SPACE to capture)', frame)
            
            # Wait for key press
            key = cv2.waitKey(1) & 0xFF
            
            # Space key to capture
            if key == 32:  # ASCII for space
                cv2.imwrite(temp_filename, frame)
                print("Image captured successfully")
                break
                
            # ESC key to exit
            if key == 27:  # ASCII for escape
                print("Capture cancelled")
                cv2.destroyAllWindows()
                return None
        
        cv2.destroyAllWindows()
        
        return temp_filename
    
    def read_frame(self):
        """Read a single frame from the camera"""
        if not self.cap or not self.cap.isOpened():
            self.open()
        
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Could not read frame from camera")
        return frame 