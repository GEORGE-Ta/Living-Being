# Thinking AI

A sophisticated AI simulation that implements continuous thought processes and desire-driven behavior.

## Features

- **Continuous Thinking Process**: Simulates ongoing thought generation and self-reflection
- **Desire System**: Implements a flexible system of desires and goals that guide the AI's behavior
- **Multi-LLM Support**: Compatible with both Ollama and OpenAI language models
- **Persistent Storage**: Stores thoughts and desires in a SQLite database
- **REST API**: Full-featured API for interaction and control

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/thinking-ai.git
cd thinking-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python -m app.main
```

## API Endpoints

- `POST /start` - Start the thinking process
- `POST /stop` - Stop the thinking process
- `GET /thoughts` - Retrieve all thoughts
- `POST /desires` - Add a new desire
- `DELETE /desires/{id}` - Remove a desire
- `GET /status` - Get current system status

## Configuration

The application can be configured using environment variables:

- `OPENAI_API_KEY` - Your OpenAI API key (if using OpenAI)
- `LLM_PROVIDER` - Choose between "ollama" or "openai" (default: "ollama")
- `OLLAMA_BASE_URL` - Ollama API URL (default: "http://localhost:11434")
- `OLLAMA_MODEL` - Ollama model to use (default: "llama2")

## Testing

Run the test suite:
```bash
pytest app/tests/
```

## Project Structure

```
thinking-ai/
├── app/
│   ├── api/
│   ├── core/
│   │   └── thinking_engine.py
│   ├── models/
│   │   ├── database.py
│   │   ├── desire.py
│   │   └── thought.py
│   ├── schemas/
│   │   ├── desire.py
│   │   └── thought.py
│   ├── tests/
│   │   ├── test_api.py
│   │   └── test_thinking_engine.py
│   ├── utils/
│   │   └── llm_interface.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License
