# CSV Analyzer Agent - Refactored Version

This is a refactored version of the CSV Analyzer Agent with improved modularity and maintainability.

## Project Structure

```
csv_analyzer/
├── api/              # FastAPI endpoints
├── cache/            # Caching functionality
├── core/             # Core business logic
├── models/           # LLM models and prompt templates
├── ui/               # Streamlit user interface
├── run_api.py        # API entry point
├── run_streamlit.py  # Streamlit entry point
└── requirements.txt  # Dependencies
```

## Key Improvements

1. **Modular Design**: Code is now organized into logical modules following SOLID principles
2. **Better Configuration**: Centralized configuration management
3. **Improved Error Handling**: More robust error handling and validation
4. **Enhanced Caching**: Better cache management with SQLite
5. **Type Safety**: Comprehensive type hints throughout the codebase
6. **Testability**: More testable code with clear separation of concerns

## Installation

1. Install the dependencies:
   ```bash
   pip install -r csv_analyzer/requirements.txt
   ```

2. Set up environment variables in a `.env` file:
   ```env
   # LLM Provider (either "gemini" or "ollama")
   LLM_PROVIDER=gemini

   # For Gemini
   GOOGLE_API_KEY=your_google_api_key

   # For Ollama (optional if using Ollama)
   OLLAMA_MODEL=qwen3:0.6b
   OLLAMA_BASE_URL=http://localhost:11434
   ```

## Usage

### Running the API

```bash
python csv_analyzer/run_api.py
```

### Running the Streamlit UI

```bash
streamlit run csv_analyzer/run_streamlit.py
```

## API Endpoints

- `POST /insights/file` - Upload a file and get AI-generated insights
- `GET /insights/{cache_key}` - Retrieve previously generated insights by cache key
- `GET /health` - Health check endpoint

## Supported File Formats

- CSV
- XLSX
- XLS
- JSON