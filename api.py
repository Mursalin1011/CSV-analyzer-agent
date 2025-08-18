"""
Refactored API implementation for CSV Analyzer Agent
This file now serves as a wrapper for the new modular implementation
"""

from csv_analyzer.api.main import api_app
from csv_analyzer.core.analyzer import DataAnalyzer
from csv_analyzer.cache.cache_manager import CacheManager

# For backward compatibility
app_graph = DataAnalyzer().workflow
cache_manager = CacheManager()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api_app, host="127.0.0.1", port=8000)