import os
import sys
from dotenv import load_dotenv

def test_gemini():
    print("Testing Gemini model...")
    # Set environment variable
    os.environ["LLM_PROVIDER"] = "gemini"
    
    # Clear any cached imports
    modules_to_clear = [k for k in sys.modules.keys() if k.startswith('api') or k.startswith('langchain')]
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    try:
        from api import llm as gemini_llm
        print("Gemini model loaded successfully")
        print(f"Gemini model type: {type(gemini_llm)}")
        return True
    except Exception as e:
        print(f"Error loading Gemini model: {e}")
        return False

def test_ollama():
    print("\nTesting Ollama model...")
    # Set environment variable
    os.environ["LLM_PROVIDER"] = "ollama"
    
    # Clear any cached imports
    modules_to_clear = [k for k in sys.modules.keys() if k.startswith('api') or k.startswith('langchain')]
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    try:
        from api import llm as ollama_llm
        print("Ollama model loaded successfully")
        print(f"Ollama model type: {type(ollama_llm)}")
        return True
    except Exception as e:
        print(f"Error loading Ollama model: {e}")
        return False

if __name__ == "__main__":
    load_dotenv()
    
    # Test both models
    gemini_success = test_gemini()
    ollama_success = test_ollama()
    
    print("\n" + "="*50)
    if gemini_success and ollama_success:
        print("Both models loaded successfully!")
        print("To switch between models, update the LLM_PROVIDER in your .env file")
    else:
        print("There were issues loading one or both models.")
        if not gemini_success:
            print("- Gemini model failed to load")
        if not ollama_success:
            print("- Ollama model failed to load")