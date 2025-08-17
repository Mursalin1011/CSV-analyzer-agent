# Test API endpoints
import os
import sys
import pandas as pd
from io import StringIO, BytesIO
from dotenv import load_dotenv

# Add parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_api_endpoints_gemini():
    """Test API endpoints with Gemini model"""
    print("Testing API endpoints with Gemini model...")
    os.environ["LLM_PROVIDER"] = "gemini"
    
    # Clear module cache
    modules_to_clear = [k for k in sys.modules.keys() if k.startswith('api') or k.startswith('langchain')]
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    try:
        from api import api_app
        from fastapi.testclient import TestClient
        import json
        
        client = TestClient(api_app)
        
        # Create a simple CSV file for testing
        csv_content = """name,age,salary,department
John,30,50000,Engineering
Jane,25,60000,Marketing
Bob,35,70000,Sales
Alice,28,55000,Engineering
Charlie,32,65000,Marketing"""
        
        # Test file upload endpoint
        files = {'file': ('test.csv', csv_content, 'text/csv')}
        response = client.post("/insights/file", files=files)
        
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        response_data = response.json()
        assert "insights" in response_data, "Response should contain 'insights'"
        assert "cache_key" in response_data, "Response should contain 'cache_key'"
        assert isinstance(response_data["insights"], str), "Insights should be a string"
        assert len(response_data["insights"]) > 0, "Insights should not be empty"
        
        cache_key = response_data["cache_key"]
        
        # Test get insights endpoint
        response = client.get(f"/insights/{cache_key}")
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        response_data = response.json()
        assert "insights" in response_data, "Response should contain 'insights'"
        assert "cache_key" in response_data, "Response should contain 'cache_key'"
        assert response_data["cache_key"] == cache_key, "Cache key should match"
        
        print("PASS: API endpoints with Gemini model work correctly")
        return True
    except Exception as e:
        print(f"FAIL: Error testing API endpoints with Gemini: {e}")
        return False

def test_api_endpoints_ollama():
    """Test API endpoints with Ollama model"""
    print("Testing API endpoints with Ollama model...")
    os.environ["LLM_PROVIDER"] = "ollama"
    
    # Clear module cache
    modules_to_clear = [k for k in sys.modules.keys() if k.startswith('api') or k.startswith('langchain')]
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    try:
        from api import api_app
        from fastapi.testclient import TestClient
        import json
        
        client = TestClient(api_app)
        
        # Create a simple CSV file for testing
        csv_content = """name,age,salary,department
John,30,50000,Engineering
Jane,25,60000,Marketing
Bob,35,70000,Sales
Alice,28,55000,Engineering
Charlie,32,65000,Marketing"""
        
        # Test file upload endpoint
        files = {'file': ('test.csv', csv_content, 'text/csv')}
        response = client.post("/insights/file", files=files)
        
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        response_data = response.json()
        assert "insights" in response_data, "Response should contain 'insights'"
        assert "cache_key" in response_data, "Response should contain 'cache_key'"
        assert isinstance(response_data["insights"], str), "Insights should be a string"
        assert len(response_data["insights"]) > 0, "Insights should not be empty"
        
        cache_key = response_data["cache_key"]
        
        # Test get insights endpoint
        response = client.get(f"/insights/{cache_key}")
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        response_data = response.json()
        assert "insights" in response_data, "Response should contain 'insights'"
        assert "cache_key" in response_data, "Response should contain 'cache_key'"
        assert response_data["cache_key"] == cache_key, "Cache key should match"
        
        print("PASS: API endpoints with Ollama model work correctly")
        return True
    except Exception as e:
        print(f"FAIL: Error testing API endpoints with Ollama: {e}")
        return False

if __name__ == "__main__":
    load_dotenv()
    
    print("Testing API endpoints with both models")
    print("=" * 50)
    
    # Test API endpoints with both models
    api_gemini_success = test_api_endpoints_gemini()
    api_ollama_success = test_api_endpoints_ollama()
    
    print("\n" + "=" * 50)
    print("API Endpoint Test Results:")
    print(f"API endpoints with Gemini: {'PASS' if api_gemini_success else 'FAIL'}")
    print(f"API endpoints with Ollama: {'PASS' if api_ollama_success else 'FAIL'}")
    
    all_passed = api_gemini_success and api_ollama_success
    
    if all_passed:
        print("\nAll API endpoint tests passed!")
    else:
        print("\nSome API endpoint tests failed.")