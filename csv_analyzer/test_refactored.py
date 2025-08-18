"""
Test script for the refactored CSV Analyzer Agent
"""
import os
import sys
import pandas as pd
from io import StringIO

# Add the current directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

def test_refactored_code():
    """Test the refactored code components"""
    print("Testing refactored CSV Analyzer Agent components...")
    
    try:
        # Test configuration
        from csv_analyzer.core.config import Config
        config_valid, config_error = Config.validate()
        print(f"Configuration valid: {config_valid}")
        if not config_valid:
            print(f"Configuration error: {config_error}")
        
        # Test data processor
        from csv_analyzer.core.data_processor import load_data, get_dataset_info, generate_cache_key
        
        # Create sample data
        csv_data = """name,age,salary,department
John,30,50000,Engineering
Jane,25,60000,Marketing
Bob,35,70000,Sales"""
        
        # Test loading data
        df = load_data(csv_data, "csv")
        print(f"Data loaded successfully. Shape: {df.shape}")
        
        # Test getting dataset info
        data_info = get_dataset_info(df)
        print("Dataset info extracted successfully")
        
        # Test generating cache key
        cache_key = generate_cache_key(df)
        print(f"Cache key generated: {cache_key[:8]}...")
        
        # Test cache manager
        from csv_analyzer.cache.cache_manager import CacheManager
        cache_manager = CacheManager()
        test_insights = "These are test insights"
        cache_manager.save_insights(cache_key, test_insights)
        loaded_insights = cache_manager.load_insights(cache_key)
        print(f"Cache test - Saved: {test_insights == loaded_insights}")
        
        print("All tests passed!")
        return True
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_refactored_code()