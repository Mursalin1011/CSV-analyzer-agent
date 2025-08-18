import pandas as pd
import hashlib
from io import StringIO, BytesIO
from typing import Union, Dict, Any

def load_data(file_data: Union[str, bytes], file_extension: str) -> pd.DataFrame:
    """Load data from various file formats"""
    loaders = {
        "csv": lambda data: pd.read_csv(StringIO(data) if isinstance(data, str) else data),
        "xlsx": lambda data: pd.read_excel(BytesIO(data) if isinstance(data, bytes) else data),
        "xls": lambda data: pd.read_excel(BytesIO(data) if isinstance(data, bytes) else data),
        "json": lambda data: pd.read_json(StringIO(data) if isinstance(data, str) else data),
    }
    
    if file_extension not in loaders:
        raise ValueError(f"Unsupported file format: {file_extension}")
    
    return loaders[file_extension](file_data)

def get_dataset_info(df: pd.DataFrame) -> Dict[str, Any]:
    """Extract key information from a dataset"""
    columns_info = ", ".join(df.columns.tolist())
    # Limit stats to essential metrics to reduce token usage
    stats_summary = df.describe().loc[['count', 'mean', 'std']].to_string()  # Only key stats
    # Limit data sample to reduce token usage
    data_sample = df.head(5).to_string(index=False)  # Reduced from 10 to 5 rows
    
    return {
        "columns": columns_info,
        "stats_summary": stats_summary,
        "data_sample": data_sample
    }

def generate_cache_key(df: pd.DataFrame) -> str:
    """Generate a cache key for a dataset"""
    # Use a smaller sample for cache key to reduce computation
    sample = df.head(3).to_string(index=False)  # Reduced from 10 to 3 rows
    return hashlib.md5(sample.encode()).hexdigest()