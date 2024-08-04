# Personal Voice Assistant

This is a personal voice assistant that can perform various tasks such as playing music from YouTube, fixing errors, and chatting with you like a normal chatbot. The assistant is built using Python and leverages several libraries and APIs to provide its functionalities.

# Preview

[Watch the video](preview.mp4)

## Features

1. **Play Music from YouTube**: You can ask the assistant to play music from YouTube based on a search query.
2. **Fix Errors**: The assistant can take a screenshot, extract text from the image, and attempt to fix any errors found in the text.
3. **Chatbot**: The assistant can engage in normal conversations with you.

## Getting Started

### Prerequisites

Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
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


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [GroqApi](https://groq.com/)
- [Meta](https://github.com/meta-llama/llama3)
- [DataCamp](https://www.datacamp.com/)