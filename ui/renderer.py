import cv2

class TextRenderer:
    """Handles text rendering with wrapping and formatting"""
    
    @staticmethod
    def wrap_text(text, font_face, font_scale, max_width):
        """Split text into lines that fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            # Try adding the word to the current line
            test_line = ' '.join(current_line + [word])
            # Get width of this test line
            (text_width, _), _ = cv2.getTextSize(test_line, font_face, font_scale, 1)
            
            if text_width <= max_width:
                # Word fits, add it to the current line
                current_line.append(word)
            else:
                # Word doesn't fit, start a new line
                if current_line:  # Don't add empty lines
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        # Add the last line if it's not empty
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    @staticmethod
    def render_result_overlay(frame, question_text, results, is_processing):
        """Render an overlay with question and results on the frame"""
        # Create a copy for display
        display_frame = frame.copy()
            
        # Display instructions
        cv2.putText(display_frame, "RobbingHood | SPACE to capture, ESC for menu", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if is_processing:
            cv2.putText(display_frame, "Processing...", 
                       (10, display_frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4)
            cv2.putText(display_frame, "Processing...", 
                       (10, display_frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Create a black background overlay at the bottom if we have results
        if question_text:
            height, width = display_frame.shape[:2]
            overlay_height = min(250, height // 2)
            overlay = display_frame.copy()
            cv2.rectangle(overlay, (0, height-overlay_height), (width, height), (0, 0, 0), -1)
            
            # Apply the overlay with some transparency
            alpha = 0.7
            cv2.addWeighted(overlay, alpha, display_frame, 1-alpha, 0, display_frame)
            
            # Format question text for display
            short_question = question_text[:100] + "..." if len(question_text) > 100 else question_text
            
            # Calculate how many models have results
            models_completed = sum(1 for model in results.values() if model["result"] is not None)
            
            # Show progress or results header
            header_text = f"Triple Check Progress: {models_completed}/3" if is_processing else "Triple Check Results"
            cv2.putText(display_frame, header_text, 
                      (10, height-overlay_height+30), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Show question snippet
            cv2.putText(display_frame, f"Q: {short_question}", 
                      (10, height-overlay_height+70), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            
            # Display results that have come in
            y_pos = height-overlay_height+110
            
            # Display all model results
            for model_name, color in [
                ("gpt4", (255, 200, 0)),      # GPT-4 in yellowish
                ("sonar_pro", (0, 255, 100)),  # Sonar Pro in green
                ("sonar", (0, 200, 255))       # Sonar in orange
            ]:
                model_data = results[model_name]
                display_name = "GPT-4" if model_name == "gpt4" else model_name.replace("_", " ").title()
                
                if not is_processing and not model_data["result"]:
                    continue
                    
                model_text = f"{display_name}: {model_data['result']} ({model_data['time']:.2f}s)" if model_data["result"] else f"{display_name}: Processing..."
                cv2.putText(display_frame, model_text, (10, y_pos), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                y_pos += 40
            
            # Show consensus if all are in
            if models_completed == 3:
                gpt4_result = results["gpt4"]["result"]
                sonar_pro_result = results["sonar_pro"]["result"]
                sonar_result = results["sonar"]["result"]
                
                if gpt4_result == sonar_pro_result == sonar_result:
                    cv2.putText(display_frame, "All models agree!", (10, y_pos), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                else:
                    cv2.putText(display_frame, "models disagree - check console", (10, y_pos), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        return display_frame 