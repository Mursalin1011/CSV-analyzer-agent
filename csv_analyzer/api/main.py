from fastapi import FastAPI, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import pandas as pd
from io import StringIO, BytesIO
from csv_analyzer.core.config import Config
from csv_analyzer.core.data_processor import load_data, get_dataset_info, generate_cache_key
from csv_analyzer.core.analyzer import DataAnalyzer

# Initialize configuration
config_valid, config_error = Config.validate()
if not config_valid:
    raise RuntimeError(f"Configuration error: {config_error}")

# Create FastAPI app
api_app = FastAPI(
    title=Config.APP_TITLE,
    description=Config.APP_DESCRIPTION,
    version="1.0.0"
)

# Add CORS middleware
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzer
analyzer = DataAnalyzer()

@api_app.post("/insights/file", response_model=Dict[str, Any])
async def upload_file(file: UploadFile):
    """Upload a file and get AI-generated insights"""
    try:
        # Determine file extension
        file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
        
        # Read file content
        content = await file.read()
        
        # Load data
        if file_extension in ['csv']:
            df = load_data(content.decode('utf-8'), file_extension)
        else:
            df = load_data(content, file_extension)
        
        # Get dataset info
        data_info = get_dataset_info(df)
        
        # Generate cache key
        cache_key = generate_cache_key(df)
        
        # Analyze data with caching
        insights = analyzer.analyze_with_caching(data_info, cache_key)
        
        return {
            "insights": insights,
            "cache_key": cache_key
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )

@api_app.get("/insights/{cache_key}", response_model=Dict[str, Any])
async def get_insights(cache_key: str):
    """Retrieve previously generated insights by cache key"""
    try:
        insights = analyzer.cache_manager.load_insights(cache_key)
        if not insights:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insights not found for the provided cache key"
            )
        
        return {
            "insights": insights,
            "cache_key": cache_key
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving insights: {str(e)}"
        )

@api_app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}