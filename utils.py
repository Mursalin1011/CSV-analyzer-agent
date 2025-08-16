import json
import os
from typing import Dict, Any

# File path for JSON cache
INSIGHTS_CACHE_FILE = "insights_cache.json"

def save_insights_to_file(cache_key: str, insights: str):
    """Save insights to JSON file with error handling"""
    # Load existing data
    try:
        with open(INSIGHTS_CACHE_FILE, "r") as f:
            content = f.read().strip()
            if content:  # Check if file is not empty
                data = json.loads(content)
            else:
                data = {}
    except FileNotFoundError:
        data = {}
    except json.JSONDecodeError:
        # Handle corrupted or invalid JSON files
        data = {}
    except Exception as e:
        print(f"Unexpected error reading cache file: {e}")
        data = {}
    
    # Update with new insights
    data[cache_key] = insights
    
    # Save back to file with error handling
    try:
        with open(INSIGHTS_CACHE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error writing to cache file: {e}")
        # We don't raise an exception here because we still want to return the insights to the user

def load_insights_from_file(cache_key: str) -> str:
    """Load insights from JSON file with error handling"""
    try:
        with open(INSIGHTS_CACHE_FILE, "r") as f:
            content = f.read().strip()
            if content:  # Check if file is not empty
                data = json.loads(content)
                return data.get(cache_key, None)
            else:
                return None
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        # Handle corrupted or invalid JSON files
        return None
    except Exception as e:
        print(f"Unexpected error loading from cache file: {e}")
        return None