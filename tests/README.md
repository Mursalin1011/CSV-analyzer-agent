# Tests Directory

This directory contains comprehensive tests for the CSV Analyzer Agent application.

## Test Files

1. `comprehensive_test.py` - Tests both API and Streamlit applications with both Gemini and Ollama models
2. `test_api_endpoints.py` - Tests the FastAPI endpoints with file upload and retrieval
3. `test_database.py` - Tests the SQLite database functionality
4. `test_end_to_end.py` - End-to-end tests for both models
5. `test_llm_responses.py` - Tests the response formats from both LLMs
6. `test_models.py` - Tests model loading for both Gemini and Ollama
7. `test_trial_models.py` - Tests model loading in the trial1.py file

## Running Tests

To run all tests, execute from the project root directory:

```bash
# Activate virtual environment
.\env\Scripts\activate

# Run individual tests
python tests/comprehensive_test.py
python tests/test_api_endpoints.py
python tests/test_database.py
```

## Test Results

All tests should pass with both LLM providers:
- Google Gemini (requires API key)
- Ollama with qwen3:0.6b model (requires Ollama running locally)

The application correctly handles the different response formats from both models:
- Gemini returns `AIMessage` objects with a `content` attribute
- Ollama returns plain strings directly