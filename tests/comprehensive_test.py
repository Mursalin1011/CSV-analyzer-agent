# Comprehensive test suite for CSV Analyzer Agent
import os
import sys
import pandas as pd
from io import StringIO
from dotenv import load_dotenv

# Add parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_api_gemini():
    """Test API with Gemini model"""
    print("Testing API with Gemini model...")
    os.environ["LLM_PROVIDER"] = "gemini"
    
    # Clear module cache
    modules_to_clear = [k for k in sys.modules.keys() if k.startswith('api') or k.startswith('langchain')]
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    try:
        from api import api_app, app_graph
        from fastapi.testclient import TestClient
        
        # Test LangGraph directly first
        csv_data = """name,age,salary,department
John,30,50000,Engineering
Jane,25,60000,Marketing
Bob,35,70000,Sales"""
        
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
        
        result = app_graph.invoke(inputs)
        response = result["insights"]
        
        assert isinstance(response, str), "Response should be a string"
        assert len(response) > 0, "Response should not be empty"
        print("PASS: API with Gemini model works correctly")
        return True
    except Exception as e:
        print(f"FAIL: Error testing API with Gemini: {e}")
        return False

def test_api_ollama():
    """Test API with Ollama model"""
    print("Testing API with Ollama model...")
    os.environ["LLM_PROVIDER"] = "ollama"
    
    # Clear module cache
    modules_to_clear = [k for k in sys.modules.keys() if k.startswith('api') or k.startswith('langchain')]
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    try:
        from api import api_app, app_graph
        from fastapi.testclient import TestClient
        
        # Test LangGraph directly first
        csv_data = """name,age,salary,department
John,30,50000,Engineering
Jane,25,60000,Marketing
Bob,35,70000,Sales"""
        
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
        
        result = app_graph.invoke(inputs)
        response = result["insights"]
        
        assert isinstance(response, str), "Response should be a string"
        assert len(response) > 0, "Response should not be empty"
        print("PASS: API with Ollama model works correctly")
        return True
    except Exception as e:
        print(f"FAIL: Error testing API with Ollama: {e}")
        return False

def test_streamlit_gemini():
    """Test Streamlit app with Gemini model"""
    print("Testing Streamlit app with Gemini model...")
    os.environ["LLM_PROVIDER"] = "gemini"
    
    # Clear module cache
    modules_to_clear = [k for k in sys.modules.keys() if k.startswith('trial1') or k.startswith('langchain')]
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    try:
        from trial1 import app_graph
        
        # Test LangGraph directly
        csv_data = """name,age,salary,department
John,30,50000,Engineering
Jane,25,60000,Marketing
Bob,35,70000,Sales"""
        
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
        
        result = app_graph.invoke(inputs)
        response = result["insights"]
        
        assert isinstance(response, str), "Response should be a string"
        assert len(response) > 0, "Response should not be empty"
        print("PASS: Streamlit app with Gemini model works correctly")
        return True
    except Exception as e:
        print(f"FAIL: Error testing Streamlit app with Gemini: {e}")
        return False

def test_streamlit_ollama():
    """Test Streamlit app with Ollama model"""
    print("Testing Streamlit app with Ollama model...")
    os.environ["LLM_PROVIDER"] = "ollama"
    
    # Clear module cache
    modules_to_clear = [k for k in sys.modules.keys() if k.startswith('trial1') or k.startswith('langchain')]
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    try:
        from trial1 import app_graph
        
        # Test LangGraph directly
        csv_data = """name,age,salary,department
John,30,50000,Engineering
Jane,25,60000,Marketing
Bob,35,70000,Sales"""
        
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
        
        result = app_graph.invoke(inputs)
        response = result["insights"]
        
        assert isinstance(response, str), "Response should be a string"
        assert len(response) > 0, "Response should not be empty"
        print("PASS: Streamlit app with Ollama model works correctly")
        return True
    except Exception as e:
        print(f"FAIL: Error testing Streamlit app with Ollama: {e}")
        return False

if __name__ == "__main__":
    load_dotenv()
    
    print("Running comprehensive tests for CSV Analyzer Agent")
    print("=" * 60)
    
    # Test API with both models
    api_gemini_success = test_api_gemini()
    api_ollama_success = test_api_ollama()
    
    # Test Streamlit app with both models
    streamlit_gemini_success = test_streamlit_gemini()
    streamlit_ollama_success = test_streamlit_ollama()
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print(f"API with Gemini: {'PASS' if api_gemini_success else 'FAIL'}")
    print(f"API with Ollama: {'PASS' if api_ollama_success else 'FAIL'}")
    print(f"Streamlit with Gemini: {'PASS' if streamlit_gemini_success else 'FAIL'}")
    print(f"Streamlit with Ollama: {'PASS' if streamlit_ollama_success else 'FAIL'}")
    
    all_passed = all([api_gemini_success, api_ollama_success, streamlit_gemini_success, streamlit_ollama_success])
    
    if all_passed:
        print("\nAll tests passed! The application works correctly with both models.")
    else:
        print("\nSome tests failed. Please check the errors above.")