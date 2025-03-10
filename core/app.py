import os
import time
import threading
import concurrent.futures
import cv2

class RobbinHoodApp:
    """Main application class coordinating the RobbinHood app workflow"""
    
    def __init__(self, config, camera_manager, ocr_processor, display_manager):
        self.config = config
        self.camera_manager = camera_manager
        self.ocr_processor = ocr_processor
        self.display_manager = display_manager
        
        from ai.perplexity import PerplexityProcessor
        from ai.gpt4 import GPT4Processor
        
        self.ai_processors = {
            "gpt4": GPT4Processor(config.openai_api_key),
            "sonar_pro": PerplexityProcessor(config.perplexity_api_key, model="sonar-pro"),
            "sonar": PerplexityProcessor(config.perplexity_api_key, model="sonar")
        }
    
    def run(self):
        """Run the main application loop"""
        print("Robbinhood initialized.")
        
        while True:
            print("\nOptions:")
            print("1. Sonar Pro (less credits used)")
            print("2. Triple check mode (uses more api credits be careful)")
            print("3. Change camera")
            print("4. Exit")
            choice = input("Enter your choice (1-4): ")
            
            if choice == '1':
                self.continuous_capture_and_process()
                
            elif choice == '2':
                self.continuous_triple_check()
                
            elif choice == '3':
                self.change_camera()
                
            elif choice == '4':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def change_camera(self):
        """Change the active camera"""
        available_cameras = self.camera_manager.list_available_cameras()
        if not available_cameras:
            print("No cameras detected.")
            return
        
        print("\nAvailable cameras:")
        for i, (idx, name) in enumerate(available_cameras):
            print(f"{i+1}. {name}")
        
        try:
            selection = int(input(f"Select camera (1-{len(available_cameras)}): "))
            if 1 <= selection <= len(available_cameras):
                selected_idx, selected_name = available_cameras[selection-1]
                self.camera_manager.camera_index = selected_idx
                self.camera_manager.camera_name = selected_name
                self.camera_manager.release()
                print(f"{selected_name} selected.")
            else:
                print("Invalid selection. No changes made.")
        except ValueError:
            print("Invalid input. No changes made.")
    
    def continuous_capture_and_process(self):
        """Continuously capture and process images until ESC is pressed"""
        print("Starting continuous capture mode. Press SPACE to capture an image, ESC to return to menu.")
        
        self.camera_manager.open()
        
        last_result = None
        is_processing = False
        processing_start_time = 0
        
        ocr_time = None
        api_time = None
        total_time = None
        
        try:
            while True:
                frame = self.camera_manager.read_frame()
                
                display_frame = frame.copy()
                    
                cv2.putText(display_frame, "Welcome to Robbinghood. SPACE to capture. ESC to return to menu", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                if is_processing:
                    elapsed_time = time.time() - processing_start_time
                    cv2.putText(display_frame, f"Processing... ({elapsed_time:.1f}s)", 
                                (10, display_frame.shape[0] - 20), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4)
                    cv2.putText(display_frame, f"Processing... ({elapsed_time:.1f}s)", 
                                (10, display_frame.shape[0] - 20), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                elif last_result:
                    font_scale = 0.7  # Slightly larger font
                    font_face = cv2.FONT_HERSHEY_SIMPLEX
                    line_spacing = 30  # Increased line spacing
                    margin = 15  # Increased margin
                    padding = 10  # Extra padding around text
                    
                    # Calculate maximum width for text wrapping
                    max_text_width = display_frame.shape[1] - 2 * margin - 2 * padding
                    
                    # Prepare answer text with "Answer: " prefix
                    full_text = f"Answer: {last_result}"
                    
                    # Wrap text into multiple lines
                    lines = self.display_manager.renderer.wrap_text(full_text, font_face, font_scale, max_text_width)
                    
                    # Add timing information lines if available
                    if total_time is not None:
                        lines.append("")  # Add spacing
                        lines.append(f"OCR: {ocr_time:.2f}s | API: {api_time:.2f}s | Total: {total_time:.2f}s")
                    
                    # Calculate background dimensions with padding
                    text_height = len(lines) * line_spacing
                    
                    # Get text metrics to ensure proper alignment
                    baseline = 0
                    for line in lines:
                        (text_width, text_height_line), baseline_line = cv2.getTextSize(
                            line, font_face, font_scale, 1)
                        if baseline_line > baseline:
                            baseline = baseline_line
                    
                    # Adjusted background rectangle with proper padding
                    bg_y1 = int(display_frame.shape[0] - text_height - 2 * padding - margin)
                    bg_y2 = int(display_frame.shape[0] - margin + padding)
                    
                    cv2.rectangle(display_frame, 
                                 (int(margin - padding), bg_y1),
                                 (int(display_frame.shape[1] - margin + padding), bg_y2),
                                 (0, 0, 0), -1)
                    
                    # Draw each line of text with proper vertical positioning
                    for i, line in enumerate(lines):
                        # Calculate text position and convert to integers
                        y_position = int(bg_y1 + padding + (i + 0.7) * line_spacing)
                        
                        # Set color based on line content (make timing info a different color)
                        text_color = (200, 200, 255) if "OCR:" in line else (255, 255, 255)
                        
                        # Draw the text with a slight shadow effect for better readability
                        cv2.putText(display_frame, line, 
                                    (int(margin), y_position), 
                                    font_face, font_scale, (40, 40, 40), 2)  # Subtle shadow
                        cv2.putText(display_frame, line, 
                                    (int(margin), y_position), 
                                    font_face, font_scale, text_color, 1)  # White/colored text
                
                # Show the frame
                cv2.imshow('Continuous Capture Mode (OCR+Perplexity)', display_frame)
                
                # Wait for key press
                key = cv2.waitKey(1) & 0xFF
                
                # ESC key to exit
                if key == 27:  # ASCII for escape
                    print("Returning to menu...")
                    break
                    
                # Space key to capture and process
                if key == 32 and not is_processing:  # ASCII for space
                    # Save the current frame
                    temp_filename = "temp_capture.jpg"
                    cv2.imwrite(temp_filename, frame)
                    print("\nImage captured, processing...")
                    
                    # Set processing flag and start time
                    is_processing = True
                    processing_start_time = time.time()
                    
                    # Two-step process: OCR then Perplexity
                    ocr_start_time = time.time()
                    extracted_text = self.ocr_processor.extract_text(temp_filename)
                    ocr_end_time = time.time()
                    ocr_time = ocr_end_time - ocr_start_time
                    
                    if extracted_text:
                        print(f"\nExtracted text ({ocr_time:.2f}s):")
                        print("-" * 40)
                        print(extracted_text)
                        print("-" * 40)
                        
                        # Process with Perplexity
                        perplexity_start_time = time.time()
                        perplexity_result = self.ai_processors["sonar_pro"].process_text(extracted_text)
                        perplexity_end_time = time.time()
                        api_time = perplexity_end_time - perplexity_start_time
                        
                        # Update last result and reset processing flag
                        last_result = perplexity_result["result"]
                        
                        # Display result in terminal too
                        print("\n" + "="*40)
                        print("RESULT:")
                        print(last_result)
                        print("="*40 + "\n")
                        
                        print(f"OCR time: {ocr_time:.2f}s")
                        print(f"Perplexity time: {api_time:.2f}s")
                    else:
                        last_result = "Failed to extract text from image"
                        ocr_time = ocr_end_time - ocr_start_time
                        api_time = 0
                    
                    # Clean up temporary file
                    if os.path.exists(temp_filename):
                        os.remove(temp_filename)
                    
                    is_processing = False
                    
                    end_time = time.time()
                    total_time = end_time - processing_start_time
                    print(f"Total processing time: {total_time:.2f} seconds")
                    print("Ready for next capture. Press SPACE to capture or ESC to return to menu.")
        
        finally:
            # Release resources
            self.camera_manager.release()
    
    def continuous_triple_check(self):
        """Continuously capture images and perform triple-check analysis until ESC is pressed"""
        print("Starting continuous triple-check mode. Press SPACE to capture an image, ESC to return to menu.")
        
        self.camera_manager.open()
        
        # Variables to store processing status and results
        is_processing = False
        has_results = False  # Flag to track if we have results to display
        processing_start_time = 0
        current_question = None
        
        # Results dictionary (will be updated during processing)
        results = {
            "gpt4": {"result": None, "time": None},
            "sonar_pro": {"result": None, "time": None},
            "sonar": {"result": None, "time": None}
        }
        
        # Flag to track if processing is complete
        processing_complete = True
        
        try:
            while True:
                frame = self.camera_manager.read_frame()
                
                # Render the UI with current state
                display_frame = self.display_manager.renderer.render_result_overlay(
                    frame, current_question, results, is_processing)
                
                cv2.imshow('Continuous Triple Check Mode', display_frame)
                
                # Wait for key press
                key = cv2.waitKey(1) & 0xFF
                
                # ESC key to exit
                if key == 27:  # ASCII for escape
                    print("Returning to menu...")
                    break
                
                # Space key to capture and process (only if not already processing)
                if key == 32 and not is_processing:  # ASCII for space
                    # Set processing flags
                    is_processing = True
                    has_results = False  # Clear previous results flag
                    processing_start_time = time.time()
                    processing_complete = False
                    current_question = None
                    
                    # Reset results for new capture
                    for key in results:
                        results[key] = {"result": None, "time": None}
                    
                    # Save the current frame
                    temp_filename = "temp_capture.jpg"
                    cv2.imwrite(temp_filename, frame)
                    print("\nImage captured, processing...")
                    
                    # Process in background thread to keep UI responsive
                    def process_image_thread():
                        nonlocal is_processing, current_question, processing_complete, has_results
                        
                        try:
                            # Extract text with OCR
                            ocr_start_time = time.time()
                            extracted_text = self.ocr_processor.extract_text(temp_filename)
                            ocr_end_time = time.time()
                            
                            # Clean up temporary file
                            if os.path.exists(temp_filename):
                                os.remove(temp_filename)
                            
                            if not extracted_text:
                                print("Failed to extract text from image")
                                is_processing = False
                                return
                            
                            # Store question for display
                            current_question = extracted_text
                            
                            print(f"\nExtracted text ({ocr_end_time - ocr_start_time:.2f}s):")
                            print("-" * 40)
                            print(extracted_text)
                            print("-" * 40)
                            
                            # Define tasks for parallel execution
                            def get_model_result(model_name):
                                processor = self.ai_processors[model_name]
                                result_data = processor.process_text(extracted_text)
                                
                                # Update the shared results dictionary
                                results[model_name] = result_data
                                
                                # Print result as it becomes available
                                print(f"\n{model_name.upper()} RESULT: {result_data['result']} ({result_data['time']:.2f}s)")
                            
                            # Execute tasks in parallel
                            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                                executor.submit(get_model_result, "gpt4")
                                executor.submit(get_model_result, "sonar_pro")
                                executor.submit(get_model_result, "sonar")
                                
                                # Wait for all to complete
                                executor.shutdown(wait=True)
                            
                            # Check for agreement after all results are in
                            gpt4_result = results["gpt4"]["result"]
                            sonar_pro_result = results["sonar_pro"]["result"]
                            sonar_result = results["sonar"]["result"]
                            
                            print("\n" + "="*60)
                            if gpt4_result == sonar_pro_result == sonar_result:
                                print("All models agree on the answer!")
                            elif sonar_pro_result == sonar_result:
                                print("Perplexity models agree, but GPT-4 differs")
                            elif sonar_pro_result == gpt4_result:
                                print("Sonar Pro and GPT-4 agree, but Sonar differs")
                            elif sonar_result == gpt4_result:
                                print("Sonar and GPT-4 agree, but Sonar Pro differs")
                            else:
                                print("❌ All models give different answers")
                            print("="*60 + "\n")
                            
                        finally:
                            processing_complete = True
                            has_results = True  # Set flag to show we have results
                            is_processing = False
                            print("Ready for next capture. Press SPACE to capture or ESC to return to menu.")
                    
                    # Start the processing thread
                    processing_thread = threading.Thread(target=process_image_thread)
                    processing_thread.daemon = True
                    processing_thread.start()
        
        finally:
            # Release resources
            self.camera_manager.release() 