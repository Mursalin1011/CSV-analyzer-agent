# Test database functionality
import os
import sys
import tempfile
from dotenv import load_dotenv

# Add parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_database_functionality():
    """Test database save/load operations"""
    print("Testing database functionality...")
    
    try:
        # Test database operations
        from database import save_insights_to_db, load_insights_from_db
        
        # Test data
        test_key = "test_key_123"
        test_insights = "This is a test insight for database testing."
        
        # Save to database
        save_result = save_insights_to_db(test_key, test_insights)
        assert save_result == True, "Failed to save insights to database"
        print("PASS: Save to database works correctly")
        
        # Load from database
        loaded_insights = load_insights_from_db(test_key)
        assert loaded_insights == test_insights, "Loaded insights don't match saved insights"
        print("PASS: Load from database works correctly")
        
        # Test loading non-existent key
        non_existent = load_insights_from_db("non_existent_key")
        assert non_existent is None, "Loading non-existent key should return None"
        print("PASS: Loading non-existent keys works correctly")
        
        return True
    except Exception as e:
        print(f"FAIL: Error testing database functionality: {e}")
        return False

def test_utils_integration():
    """Test utils.py integration with database"""
    print("Testing utils integration...")
    
    try:
        from utils import save_insights_to_file, load_insights_from_file
        
        # Test data
        test_key = "test_key_utils_456"
        test_insights = "This is a test insight for utils testing."
        
        # Save using utils (which uses database)
        save_insights_to_file(test_key, test_insights)
        print("PASS: Save through utils works correctly")
        
        # Load using utils (which uses database)
        loaded_insights = load_insights_from_file(test_key)
        assert loaded_insights == test_insights, "Loaded insights don't match saved insights"
        print("PASS: Load through utils works correctly")
        
        return True
    except Exception as e:
        print(f"FAIL: Error testing utils integration: {e}")
        return False

if __name__ == "__main__":
    load_dotenv()
    
    print("Testing database functionality")
    print("=" * 40)
    
    db_success = test_database_functionality()
    utils_success = test_utils_integration()
    
    print("\n" + "=" * 40)
    print("Database Test Results:")
    print(f"Database operations: {'PASS' if db_success else 'FAIL'}")
    print(f"Utils integration: {'PASS' if utils_success else 'FAIL'}")
    
    if db_success and utils_success:
        print("\nAll database tests passed!")
    else:
        print("\nSome database tests failed.")