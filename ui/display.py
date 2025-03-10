import cv2
import threading
from ui.renderer import TextRenderer

class DisplayManager:
    """Manages display and UI rendering"""
    
    def __init__(self, camera_manager):
        self.camera_manager = camera_manager
        self.renderer = TextRenderer()
    
    def display_triple_check_realtime(self, extracted_text, results, is_complete_func, window_name='Triple Check Results'):
        """Display triple check results on camera feed in real-time as they arrive"""
        print("Showing results on camera as they arrive. Press any key to return to menu.")
        
        # Format question text for display
        short_question = extracted_text[:100] + "..." if len(extracted_text) > 100 else extracted_text
        
        try:
            while not is_complete_func():
                try:
                    # Read frame
                    frame = self.camera_manager.read_frame()
                    
                    # Create a copy for display
                    display_frame = frame.copy()
                    
                    # Display title with processing indicator
                    models_completed = sum(1 for model in results.values() if model["result"] is not None)
                    cv2.putText(display_frame, f"Triple Check Results ({models_completed}/3 completed)", 
                              (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    # Create background for results
                    height, width = display_frame.shape[:2]
                    cv2.rectangle(display_frame, (0, height-200), (width, height), (0, 0, 0), -1)
                    
                    # Display results as they arrive
                    y_pos = height - 170
                    
                    # Show question snippet
                    cv2.putText(display_frame, f"Q: {short_question}", 
                              (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
                    y_pos += 40
                    
                    # GPT-4 result (blue)
                    gpt4_data = results["gpt4"]
                    gpt4_text = f"GPT-4 Turbo: {gpt4_data['result']} ({gpt4_data['time']:.2f}s)" if gpt4_data["result"] else "GPT-4 Turbo: Processing..."
                    cv2.putText(display_frame, gpt4_text, 
                              (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)
                    y_pos += 40
                    
                    # Sonar Pro result (green)
                    sonar_pro_data = results["sonar_pro"]
                    sonar_pro_text = f"Sonar Pro: {sonar_pro_data['result']} ({sonar_pro_data['time']:.2f}s)" if sonar_pro_data["result"] else "Sonar Pro: Processing..."
                    cv2.putText(display_frame, sonar_pro_text, 
                              (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 100), 2)
                    y_pos += 40
                    
                    # Sonar result (yellow)
                    sonar_data = results["sonar"]
                    sonar_text = f"Sonar: {sonar_data['result']} ({sonar_data['time']:.2f}s)" if sonar_data["result"] else "Sonar: Processing..."
                    cv2.putText(display_frame, sonar_text, 
                              (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
                    
                    # Show the frame
                    cv2.imshow(window_name, display_frame)
                    
                    # Check for key press with a short delay
                    if cv2.waitKey(100) != -1:
                        return
                    
                except cv2.error as e:
                    print(f"OpenCV error in display thread: {e}")
                    # Sleep briefly and continue
                    threading.Event().wait(0.2)
                    continue
                except Exception as e:
                    print(f"Unexpected error in display thread: {e}")
                    break
            
            # All results are in, show final display for a moment
            try:
                # Display final results for 2 more seconds
                for _ in range(20):  # 20 * 100ms = 2 seconds
                    if cv2.waitKey(100) != -1:
                        break
            except:
                pass  # Ignore errors during final display
        
        finally:
            cv2.destroyAllWindows() 