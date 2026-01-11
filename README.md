# ChatGPT CLI Interface

A simple command-line interface for interacting with OpenAI's ChatGPT API using Python.

## Features

- Interactive chat interface with ChatGPT
- Conversation history management
- Automatic token calculation and prompt truncation to stay within API limits
- Streaming response output
- Configurable creativity/temperature settings

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install required packages:
   ```bash
   pip install openai python-dotenv
   ```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Usage

Run the main script:
```bash
python chatgpt.py
```

Once running, you can:
- Type messages to chat with ChatGPT
- Type `exit` to quit the program
- Responses are streamed in real-time

## Configuration

### Model Settings
The default model is configured in `cai.py`:
- `OPEN_AI_COMPLETION_MODEL`: The OpenAI model to use (default: "text-davinci-003")
- `MAX_TOKENS_SAFE`: Maximum safe token limit to avoid API errors

### Prompt Settings
In `chatgpt.py`, you can modify:
- `ai_name`: Change the AI's name in the prompt
- `response_approx_max_words`: Control maximum response length (default: 500)
- `creativity01`: Adjust creativity/temperature (0.0-1.0, default: 0.5)

## Project Structure

- `chatgpt.py`: Main application with `ChatGptGen`, `Prompter`, and `Prompt` classes
- `cai.py`: Utility functions for token calculation and API configuration
- `README.md`: This documentation file

## Key Classes

### `ChatGptGen`
Handles API communication with OpenAI's ChatGPT.

### `Prompter`
Manages the interactive chat session and conversation history.

### `Prompt`
Represents a prompt with configurable parameters.

## Token Management

The application automatically:
- Calculates token counts for prompts and responses
- Truncates conversation history when approaching token limits
- Estimates word-to-token conversions (approximately 1.25 tokens per word)

## Error Handling

- API errors are caught and displayed with user-friendly messages
- Response streaming interruptions are handled gracefully
- Token limit breaches trigger automatic history truncation

## Limitations

- Knowledge cutoff: 2021-09 (for the default model)
- Requires internet connection for API calls
- Token estimation is approximate

## Contributing

Feel free to submit issues and pull requests for improvements.

## License

[Add your license information here]