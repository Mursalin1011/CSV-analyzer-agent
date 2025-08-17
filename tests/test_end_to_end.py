import os
import sys
import pandas as pd
from io import StringIO
from dotenv import load_dotenv

def test_gemini_end_to_end():
    print("Testing Gemini model end-to-end...")
    os.environ["LLM_PROVIDER"] = "gemini"
    
    # Clear module cache to force reimport
    modules_to_clear = [k for k in sys.modules.keys() if k.startswith('trial1') or k.startswith('langchain')]
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    try:
        from trial1 import app_graph
        
        # Create a simple test dataset
        csv_data = """name,age,salary,department
John,30,50000,Engineering
Jane,25,60000,Marketing
Bob,35,70000,Sales
Alice,28,55000,Engineering
Charlie,32,65000,Marketing"""
        
        df = pd.read_csv(StringIO(csv_data))
        
        # Prepare data for LLM
        columns_info = ", ".join(df.columns.tolist())
        stats_summary = df.describe().loc[['count', 'mean', 'std']].to_string()
        data_sample = df.head(3).to_string(index=False)
        
        # Generate insights with LangGraph
        inputs = {
            "columns": columns_info,
            "stats_summary": stats_summary,
            "data_sample": data_sample
        }
        
        print("Generating insights with Gemini...")
        result = app_graph.invoke(inputs)
        response = result["insights"]
        
        print(f"Response type: {type(response)}")
        print(f"Response length: {len(response)}")
        print(f"Response preview: {response[:200]}...")
        
        return True
    except Exception as e:
        print(f"Error testing Gemini model end-to-end: {e}")
        return False

def test_ollama_end_to_end():
    print("\nTesting Ollama model end-to-end...")
    os.environ["LLM_PROVIDER"] = "ollama"
    
    # Clear module cache to force reimport
    modules_to_clear = [k for k in sys.modules.keys() if k.startswith('trial1') or k.startswith('langchain')]
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    try:
        from trial1 import app_graph
        
        # Create a simple test dataset
        csv_data = """name,age,salary,department
John,30,50000,Engineering
Jane,25,60000,Marketing
Bob,35,70000,Sales
Alice,28,55000,Engineering
Charlie,32,65000,Marketing"""
        
        df = pd.read_csv(StringIO(csv_data))
        
        # Prepare data for LLM
        columns_info = ", ".join(df.columns.tolist())
        stats_summary = df.describe().loc[['count', 'mean', 'std']].to_string()
        data_sample = df.head(3).to_string(index=False)
        
        # Generate insights with LangGraph
        inputs = {
            "columns": columns_info,
            "stats_summary": stats_summary,
            "data_sample": data_sample
        }
        
        print("Generating insights with Ollama...")
        result = app_graph.invoke(inputs)
        response = result["insights"]
        
        print(f"Response type: {type(response)}")
        print(f"Response length: {len(response)}")
        print(f"Response preview: {response[:200]}...")
        
        return True
    except Exception as e:
        print(f"Error testing Ollama model end-to-end: {e}")
        return False

if __name__ == "__main__":
    load_dotenv()
    
    print("Testing LLM end-to-end functionality...")
    print("=" * 50)
    
    gemini_success = test_gemini_end_to_end()
    ollama_success = test_ollama_end_to_end()
    
    print("\n" + "=" * 50)
    if gemini_success and ollama_success:
        print("Both models worked end-to-end successfully!")
    else:
        print("There were issues with one or both models.")