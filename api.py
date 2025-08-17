from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import pandas as pd
from io import StringIO, BytesIO
import hashlib
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.callbacks import tracing_v2_enabled
from langchain_community.cache import InMemoryCache
from langchain.globals import set_llm_cache
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from dotenv import load_dotenv
from utils import save_insights_to_file, load_insights_from_file
from database import init_db

# Load environment variables from .env file
load_dotenv()

# Configure LangSmith (uses environment variables from .env)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# Initialize caching
set_llm_cache(InMemoryCache())

# Initialize the database
init_db()

# Configuration for LLM selection
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # "gemini" or "ollama"

# Initialize LLM based on configuration
if LLM_PROVIDER == "gemini":
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1  # Reduced from 0.3 for more focused responses
    )
elif LLM_PROVIDER == "ollama":
    llm = OllamaLLM(
        model=os.getenv("OLLAMA_MODEL", "qwen3:0.5b"),  # Adjust model name if needed
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0.1
    )
else:
    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

# Prompt template for data insights
prompt_template = PromptTemplate(
    input_variables=["data_sample", "columns", "stats_summary"],
    template="""
    Analyze this dataset and provide key insights:

    Columns: {columns}
    
    Statistical Summary:
    {stats_summary}
    
    Sample Data:
    {data_sample}

    Provide:
    1. Key patterns/trends (concise)
    2. Notable correlations/anomalies
    3. Business implications (if any)
    4. Analysis recommendations
    
    Format in clear markdown with headers.
    """
)

# Define state for LangGraph
class AnalysisState(TypedDict):
    data_sample: str
    columns: str
    stats_summary: str
    insights: Annotated[str, operator.add]

# Node functions for LangGraph
def generate_insights(state: AnalysisState) -> dict:
    """Generate insights using LLM"""
    with tracing_v2_enabled():
        try:
            chain = prompt_template | llm
            result = chain.invoke({
                "columns": state["columns"],
                "stats_summary": state["stats_summary"],
                "data_sample": state["data_sample"]
            })
            
            # Handle different response types from different LLMs
            # Some LLMs return a string directly, others return an object with content attribute
            if hasattr(result, 'content'):
                insights = result.content
            else:
                insights = str(result)
                
            return {"insights": insights}
        except Exception as e:
            return {"insights": f"Error generating insights: {str(e)}"}

# Create LangGraph workflow
workflow = StateGraph(AnalysisState)
workflow.add_node("insights", generate_insights)
workflow.set_entry_point("insights")
workflow.add_edge("insights", END)

# Compile the graph
app_graph = workflow.compile()

# File format handlers
def load_csv(content):
    return pd.read_csv(StringIO(content.decode('utf-8')))

def load_excel(content):
    return pd.read_excel(BytesIO(content))

def load_json(content):
    return pd.read_json(StringIO(content.decode('utf-8')))

# File loader mapping
FILE_LOADERS = {
    "csv": load_csv,
    "xlsx": load_excel,
    "xls": load_excel,
    "json": load_json
}

# Cache key generation
def get_cache_key(df):
    # Use a smaller sample for cache key to reduce computation
    sample = df.head(3).to_string(index=False)  # Reduced from 10 to 3 rows
    return hashlib.md5(sample.encode()).hexdigest()



# FastAPI app for API endpoint with enhanced documentation
api_app = FastAPI(
    title="CSV Insights API",
    description="An API for generating AI-powered insights from CSV, Excel, and JSON files",
    version="1.0.0",
    contact={
        "name": "CSV Analyzer Team",
        # "url": "https://github.com/your-org/csv-analyzer-agent",
        # "email": "support@csv-analyzer.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

class InsightsResponse(BaseModel):
    """
    Response model for insights retrieval
    """
    insights: str
    cache_key: str

class FileUploadResponse(BaseModel):
    """
    Response model for file upload and insights generation
    """
    insights: str
    cache_key: str

@api_app.get(
    "/insights/{cache_key}", 
    response_model=InsightsResponse,
    summary="Get insights by cache key",
    description="Retrieve previously generated insights using the cache key returned from file upload",
    tags=["Insights Retrieval"]
)
async def get_insights(cache_key: str):
    """
    Get insights by cache key
    
    - **cache_key**: The unique identifier for the cached insights
    """
    insights = load_insights_from_file(cache_key)
    if insights is None:
        raise HTTPException(status_code=404, detail="Insights not found for this key")
    
    return InsightsResponse(
        insights=insights,
        cache_key=cache_key
    )

@api_app.post(
    "/insights/file", 
    response_model=FileUploadResponse,
    summary="Upload a file and get AI insights",
    description="Upload a CSV, Excel (XLSX/XLS), or JSON file to generate AI-powered insights. "
                "The API will analyze the data and return key patterns, correlations, and recommendations. "
                "Results are cached to avoid reprocessing the same file.",
    tags=["File Processing"]
)
async def upload_file_for_insights(file: UploadFile = File(...)):
    """
    Upload a file and get AI insights
    
    - **file**: The file to analyze (CSV, XLSX, XLS, or JSON)
    """
    try:
        # Determine file extension
        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension not in FILE_LOADERS:
            raise HTTPException(status_code=400, detail=f"Unsupported file format: {file_extension}")
        
        # Read file content
        content = await file.read()
        
        # Load data using appropriate loader
        df = FILE_LOADERS[file_extension](content)
        
        # Prepare data for LLM
        columns_info = ", ".join(df.columns.tolist())
        # Limit stats to essential metrics to reduce token usage
        stats_summary = df.describe().loc[['count', 'mean', 'std']].to_string()  # Only key stats
        # Limit data sample to reduce token usage
        data_sample = df.head(5).to_string(index=False)  # Reduced from 10 to 5 rows
        
        # Generate cache key
        cache_key = get_cache_key(df)
        
        # Check if already in storage
        existing_insights = load_insights_from_file(cache_key)
        if existing_insights is not None:
            return FileUploadResponse(
                insights=existing_insights,
                cache_key=cache_key
            )
        
        # Generate insights with LangGraph
        inputs = {
            "columns": columns_info,
            "stats_summary": stats_summary,
            "data_sample": data_sample
        }
        result = app_graph.invoke(inputs)
        response = result["insights"]
        
        # Store the result in database
        save_insights_to_file(cache_key, response)
        
        return FileUploadResponse(
            insights=response,
            cache_key=cache_key
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# Health check endpoint
@api_app.get(
    "/health", 
    summary="Health check",
    description="Check if the API is running and healthy",
    tags=["Health"]
)
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "llm_provider": LLM_PROVIDER}