import os
import sys
import pandas as pd
from io import StringIO, BytesIO
from dotenv import load_dotenv

# Add parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_new_endpoints():
    """Test the new endpoints for getting all insights and searching insights"""
    print("Testing new endpoints...")
    
    try:
        from api import api_app
        from fastapi.testclient import TestClient
        import json
        
        client = TestClient(api_app)
        
        # Create a simple CSV file for testing
        csv_content = """name,age,salary,department,phone
John,30,50000,Engineering,123-456-7890
Jane,25,60000,Marketing,098-765-4321
Bob,35,70000,Sales,123-456-7890
Alice,28,55000,Engineering,555-123-4567
Charlie,32,65000,Marketing,098-765-4321"""
        
        # Test file upload endpoint
        files = {'file': ('test.csv', csv_content, 'text/csv')}
        response = client.post("/insights/file", files=files)
        
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        response_data = response.json()
        assert "insights" in response_data, "Response should contain 'insights'"
        assert "cache_key" in response_data, "Response should contain 'cache_key'"
        assert isinstance(response_data["insights"], str), "Insights should be a string"
        assert len(response_data["insights"]) > 0, "Insights should not be empty"
        
        # Test get all insights endpoint
        response = client.get("/insights")
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        response_data = response.json()
        assert "insights" in response_data, "Response should contain 'insights'"
        assert isinstance(response_data["insights"], list), "Insights should be a list"
        
        # Test search insights endpoint
        # First search for something that should match
        response = client.get("/insights/search/phone")
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        response_data = response.json()
        assert "results" in response_data, "Response should contain 'results'"
        assert "count" in response_data, "Response should contain 'count'"
        
        print("PASS: New endpoints work correctly")
        return True
    except Exception as e:
        print(f"FAIL: Error testing new endpoints: {e}")
        return False

if __name__ == "__main__":
    load_dotenv()
    
    print("Testing new endpoints")
    print("=" * 50)
    
    # Test new endpoints
    success = test_new_endpoints()
    
    print("=" * 50)
    if success:
        print("New endpoints test passed!")
    else:
        print("New endpoints test failed.")