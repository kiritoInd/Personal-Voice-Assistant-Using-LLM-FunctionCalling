# Personal Voice Assistant

This is a personal voice assistant that can perform various tasks such as playing music from YouTube, fixing errors, and chatting with you like a normal chatbot. The assistant is built using Python and leverages several libraries and APIs to provide its functionalities.

# Preview

[Watch the video](preview.mp4)

## Features

1. **Play Music from YouTube**: You can ask the assistant to play music from YouTube based on a search query.
2. **Fix Errors**: The assistant can take a screenshot, extract text from the image, and attempt to fix any errors found in the text.
3. **Chatbot**: The assistant can engage in normal conversations with you.

Error Fixing Process:

When a user reports an error, the Personal Voice Assistant takes a screenshot of the current screen to capture the exact issue. This image is then processed using OpenCV to extract the text from the screenshot. The extracted text is sent to the LLaMA 3 language model, which analyzes the content and generates a relevant response or solution. The assistant then communicates the suggested fix or troubleshooting steps back to the user, ensuring a streamlined and effective resolution process.

## Getting Started

### Prerequisites

Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/kiritoInd/Personal-Voice-Assistant.git
    cd Personal-Voice-Assistant
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Environment Variables

Create a `.env` file in the root directory of the project and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key
```
## Running the Assistant
### Run the following command to start the voice assistant:
``` python main.py ```
## Usage

- **Start the Assistant**: Click the "Start Bot" button in the GUI to start the assistant.
- **Trigger Word**: Say "hello" to activate the assistant.
- **Commands**:
  - **Play Music**: "Play [song name] from YouTube."
  - **Fix Error**: "Can you fix this error?"
  - **Chat**: Engage in a normal conversation.

## Adding More Functions

You can add more functionalities to the assistant through the function calling list. Learn more about function calling at [DataCamp's OpenAI Function Calling Tutorial](https://www.datacamp.com/tutorial/open-ai-function-calling-tutorial).

You can use the same for meta LLama3 

## Adding More Functions

You can add more functionalities to the assistant through the function calling list. Learn more about function calling at [DataCamp's OpenAI Function Calling Tutorial](https://www.datacamp.com/tutorial/open-ai-function-calling-tutorial).

To add new functions, update the `function_calling_template` in the code:

```python
function_calling_template = """ 
    <tools> {
    "name": "Your Function",
    "description": "Description of the function",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
    },
    } </tools>
  """
```

## Libraries and APIs Used

- `json`
- `speech_recognition`
- `pyttsx3`
- `groq`
- `Pillow`
- `opencv-python-headless`
- `pytesseract`
- `datasets`
- `torch`
- `transformers`
- `soundfile`
- `sounddevice`
- `requests`
- `beautifulsoup4`
- `keyboard`
- `tkinter`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [GroqApi](https://groq.com/)
- [Meta](https://github.com/meta-llama/llama3)
- [DataCamp](https://www.datacamp.com/)
