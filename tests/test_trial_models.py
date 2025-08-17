import os
from dotenv import load_dotenv

def test_gemini():
    print("Testing Gemini model...")
    os.environ["LLM_PROVIDER"] = "gemini"
    
    try:
        from trial1 import llm, LLM_PROVIDER
        print(f"LLM Provider: {LLM_PROVIDER}")
        print(f"LLM Type: {type(llm)}")
        return True
    except Exception as e:
        print(f"Error loading Gemini model: {e}")
        return False

def test_ollama():
    print("\nTesting Ollama model...")
    os.environ["LLM_PROVIDER"] = "ollama"
    
    try:
        # Clear module cache to force reimport
        import sys
        modules_to_clear = [k for k in sys.modules.keys() if k.startswith('trial1') or k.startswith('langchain')]
        for module in modules_to_clear:
            if module in sys.modules:
                del sys.modules[module]
        
        from trial1 import llm, LLM_PROVIDER
        print(f"LLM Provider: {LLM_PROVIDER}")
        print(f"LLM Type: {type(llm)}")
        return True
    except Exception as e:
        print(f"Error loading Ollama model: {e}")
        return False

if __name__ == "__main__":
    load_dotenv()
    
    gemini_success = test_gemini()
    ollama_success = test_ollama()
    
    print("\n" + "="*50)
    if gemini_success and ollama_success:
        print("Both models loaded successfully!")
    else:
        print("There were issues loading one or both models.")