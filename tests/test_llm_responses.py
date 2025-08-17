import os
import sys
from dotenv import load_dotenv

def test_gemini_response():
    print("Testing Gemini model response format...")
    os.environ["LLM_PROVIDER"] = "gemini"
    
    # Clear module cache to force reimport
    modules_to_clear = [k for k in sys.modules.keys() if k.startswith('trial1') or k.startswith('langchain')]
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    try:
        from trial1 import llm, prompt_template
        from langchain_core.messages import HumanMessage
        
        # Create a simple test prompt
        test_prompt = prompt_template.format(
            columns="name, age, salary",
            stats_summary="count  100\nmean   35\nstd    10",
            data_sample="name  age  salary\nJohn  30   50000\nJane  25   60000"
        )
        
        print("Sending test request to Gemini...")
        result = llm.invoke(test_prompt)
        
        print(f"Result type: {type(result)}")
        print(f"Has 'content' attribute: {hasattr(result, 'content')}")
        
        if hasattr(result, 'content'):
            print(f"Content type: {type(result.content)}")
            print(f"Content length: {len(result.content)}")
            print(f"Content preview: {result.content[:100]}...")
        else:
            print(f"Result as string: {str(result)[:100]}...")
            
        return True
    except Exception as e:
        print(f"Error testing Gemini model: {e}")
        return False

def test_ollama_response():
    print("\nTesting Ollama model response format...")
    os.environ["LLM_PROVIDER"] = "ollama"
    
    # Clear module cache to force reimport
    modules_to_clear = [k for k in sys.modules.keys() if k.startswith('trial1') or k.startswith('langchain')]
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    try:
        from trial1 import llm, prompt_template
        
        # Create a simple test prompt
        test_prompt = prompt_template.format(
            columns="name, age, salary",
            stats_summary="count  100\nmean   35\nstd    10",
            data_sample="name  age  salary\nJohn  30   50000\nJane  25   60000"
        )
        
        print("Sending test request to Ollama...")
        result = llm.invoke(test_prompt)
        
        print(f"Result type: {type(result)}")
        print(f"Has 'content' attribute: {hasattr(result, 'content')}")
        
        if hasattr(result, 'content'):
            print(f"Content type: {type(result.content)}")
            print(f"Content length: {len(result.content)}")
            print(f"Content preview: {result.content[:100]}...")
        else:
            print(f"Result as string: {str(result)[:100]}...")
            
        return True
    except Exception as e:
        print(f"Error testing Ollama model: {e}")
        return False

if __name__ == "__main__":
    load_dotenv()
    
    print("Testing LLM response formats...")
    print("=" * 50)
    
    gemini_success = test_gemini_response()
    ollama_success = test_ollama_response()
    
    print("\n" + "=" * 50)
    if gemini_success and ollama_success:
        print("Both models responded successfully!")
    else:
        print("There were issues with one or both models.")