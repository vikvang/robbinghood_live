
# RobbingHood: an ai trivia assistant. 

Bottom of this readme contains a couple feature suggestions + ways to expand this for anyone coming across this. Would also appreciate a github star if you're reading this :)

Get search grounded, up-to-date, accurate responses for any multiple choice trivia question within seconds (less than 3 on average). It combines the power of multiple AI models to give you the best possible answer under any timed based trivia game.

## Features

- **Real-time capture and analysis**: Point your camera at the question and get instant results
- **Triple-check mode**: Cross-references answers from three different AI models:
  - OpenAI's GPT-4-Turbo
  - Perplexity's Sonar Pro
  - Perplexity's Sonar
- **Continuous capture**: Keep your camera running for seamless question-to-question transitions
- **Multi-camera support**: Select from available webcams on your device
- **On-screen results**: View answers directly in the camera feed

## Technical Overview

This application demonstrates several software engineering principles and technologies:

- **Clean Architecture**: Separation of concerns with distinct layers for UI, business logic, and data
- **SOLID Principles**: Single responsibility, dependency injection, and interface segregation
- **Concurrent Processing**: Parallel API calls using ThreadPoolExecutor for optimal performance
- **Real-time Computer Vision**: OpenCV integration for camera feeds and image processing
- **Cloud AI Integration**: Multiple AI service APIs orchestrated in a single application

### Architecture

```
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│     UI      │────▶│  Application  │────▶│ AI Services  │
│  (OpenCV)   │◀────│     Core      │◀────│ (API Calls)  │
└─────────────┘     └───────────────┘     └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │     OCR      │
                    │   Services   │
                    └──────────────┘
```


## Technologies Used

- **Python 3.8+**: Core programming language
- **OpenCV**: Camera interfacing and image processing
- **Google Cloud Vision API**: Optical Character Recognition
- **API Integrations**: OpenAI API, Perplexity API
- **Concurrent Processing**: Python's ThreadPoolExecutor
- **Environment Management**: python-dotenv for configuration

## Code Structure

```
robbinhood/
├── main.py                 # Entry point and application bootstrap
├── config.py               # Configuration management
├── camera/                 # Camera abstraction layer
│   ├── __init__.py
│   └── camera_manager.py   # Camera operations and frame capture
├── ocr/                    # Text extraction services
│   ├── __init__.py
│   └── ocr_processor.py    # OCR processing with Google Vision
├── ai/                     # AI model interfaces
│   ├── __init__.py
│   ├── base_processor.py   # Abstract base class for AI models
│   ├── perplexity.py       # Perplexity API integration
│   └── gpt4.py             # OpenAI GPT-4 integration
├── ui/                     # User interface components
│   ├── __init__.py
│   ├── display.py          # Display management
│   └── renderer.py         # Text and overlay rendering
└── core/                   # Core application logic
    ├── __init__.py
    └── app.py              # Main application workflows
```

### Design Patterns Used

- **Factory Pattern**: For creating AI processors
- **Strategy Pattern**: Different AI models implement the same interface
- **Dependency Injection**: Components receive their dependencies
- **Observer Pattern**: UI updated as results become available

## Requirements

- Python 3.8+
- Webcam
- API keys:
  - Google Cloud Vision API (for OCR)
  - Perplexity API
  - OpenAI API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vikvang/robbinghood.git
cd robbinhood
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project directory with your API keys:
```
PERPLEXITY_API_KEY=your_perplexity_api_key
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CREDENTIALS_PATH=path/to/your/google_credentials.json
```

4. Set up Google Cloud Vision API:
   - Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the Vision API
   - Create a service account and download the JSON credentials file
   - Set the path to this file in your `.env` file

## Usage

Run the program:
```bash
python main.py
```

## Performance Considerations (i tried implementing the following but could be improved)

- **Parallel Processing**: AI model requests run concurrently for maximum speed
- **Non-blocking UI**: User interface remains responsive during processing
- **Optimized OCR**: Google Vision API provides high-quality text extraction
- **Memory Management**: Temporary images are properly cleaned up

## Extending the Application (feature suggestions open to anyone to build on top of this)

The modular architecture makes it easy to:

- Add new AI models by implementing the BaseAIProcessor interface
- Support alternative OCR engines by creating new OCR processor classes
- Create custom UI visualizations by extending the renderer
- Add new processing modes to the application core
