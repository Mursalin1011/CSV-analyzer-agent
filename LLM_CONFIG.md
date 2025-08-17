# CSV Analyzer Agent - LLM Configuration

This application supports two LLM providers:
1. Google Gemini (default)
2. Ollama (local models)

## Switching Between LLM Providers

To switch between LLM providers, modify the `LLM_PROVIDER` variable in the `.env` file:

### Using Google Gemini (default)
```
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_google_api_key_here
```

### Using Ollama (local models)
```
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:0.6b
```

Make sure to comment out the GOOGLE_API_KEY line when using Ollama.

## Ollama Model Requirements

If using Ollama, ensure you have the Qwen3 model installed:
```bash
ollama pull qwen3:0.6b
```

## Model Configuration

The application is configured to use:
- `qwen3:0.6b` for Ollama
- `gemini-2.5-flash` for Google Gemini

You can modify these model names in the `api.py` and `trial1.py` files if needed.

## Files Using LLM

1. `api.py` - Main FastAPI application
2. `trial1.py` - Streamlit interface for testing

Both files use the same environment variable-based switching mechanism.