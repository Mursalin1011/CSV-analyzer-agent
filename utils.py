from database import save_insights_to_db, load_insights_from_db

def save_insights_to_file(cache_key: str, insights: str):
    """Save insights to database"""
    return save_insights_to_db(cache_key, insights)

def load_insights_from_file(cache_key: str) -> str:
    """Load insights from database"""
    return load_insights_from_db(cache_key)