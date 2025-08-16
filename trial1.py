# requirements.txt
# langchain-google-genai
# pandas
# python-dotenv
# streamlit
# openpyxl
# langsmith
# langgraph
# fastapi
# uvicorn

import os
import json
import hashlib
import pandas as pd
import streamlit as st
from io import StringIO, BytesIO
from typing import Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.callbacks import tracing_v2_enabled
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator


# Load environment variables from .env file
load_dotenv()

# Configure LangSmith (uses environment variables from .env)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# Initialize caching
set_llm_cache(InMemoryCache())

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)

# Prompt template for data insights
prompt_template = PromptTemplate(
    input_variables=["data_sample", "columns", "stats_summary"],
    template="""
    You are a data analyst expert. Analyze the following dataset information and provide key insights:

    Columns: {columns}
    
    Statistical Summary:
    {stats_summary}
    
    Sample Data:
    {data_sample}

    Please provide:
    1. Summary of key patterns and trends
    2. Notable correlations or anomalies
    3. Business implications (if applicable)
    4. Recommendations for further analysis
    
    Format your response in clear markdown with headers.
    """
)

# Define state for LangGraph
class AnalysisState(TypedDict):
    data_sample: str
    columns: str
    stats_summary: str
    insights: Annotated[str, operator.add]

# Node functions for LangGraph
def generate_insights(state: AnalysisState) -> Dict[str, Any]:
    """Generate insights using LLM"""
    with tracing_v2_enabled():
        try:
            chain = prompt_template | llm
            result = chain.invoke({
                "columns": state["columns"],
                "stats_summary": state["stats_summary"],
                "data_sample": state["data_sample"]
            })
            return {"insights": result.content}
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
def load_csv(uploaded_file):
    return pd.read_csv(uploaded_file)

def load_excel(uploaded_file):
    return pd.read_excel(uploaded_file)

def load_json(uploaded_file):
    return pd.read_json(uploaded_file)

# File loader mapping
FILE_LOADERS = {
    "csv": load_csv,
    "xlsx": load_excel,
    "xls": load_excel,
    "json": load_json
}

# Cache key generation
def get_cache_key(df):
    sample = df.head(10).to_string(index=False)
    return hashlib.md5(sample.encode()).hexdigest()

# FastAPI app for API endpoint
api_app = FastAPI(title="CSV Insights API", version="1.0.0")

class InsightsResponse(BaseModel):
    insights: str
    cache_key: str

@api_app.get("/insights/{cache_key}", response_model=InsightsResponse)
async def get_insights(cache_key: str):
    """Get insights by cache key"""
    if 'cache' not in st.session_state:
        raise HTTPException(status_code=404, detail="Cache not initialized")
    
    if cache_key not in st.session_state.cache:
        raise HTTPException(status_code=404, detail="Insights not found for this key")
    
    return InsightsResponse(
        insights=st.session_state.cache[cache_key],
        cache_key=cache_key
    )

# Streamlit UI
st.title("📊 CSV Data Insights Generator")
st.markdown("Upload your data file to get AI-powered insights using Google Gemini")

# File uploader with multiple format support
uploaded_file = st.file_uploader(
    "Upload your file", 
    type=["csv", "xlsx", "xls", "json"]
)

if uploaded_file:
    try:
        # Determine file extension
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension not in FILE_LOADERS:
            st.error(f"Unsupported file format: {file_extension}")
            st.stop()
        
        # Load data using appropriate loader
        df = FILE_LOADERS[file_extension](uploaded_file)
        
        # Display basic info
        st.subheader("Dataset Overview")
        st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        st.write("Columns:", ", ".join(df.columns.tolist()))
        
        # Show data sample
        st.subheader("Data Sample")
        st.dataframe(df.head())
        
        # Generate statistical summary
        st.subheader("Statistical Summary")
        st.write(df.describe())
        
        # Prepare data for LLM
        columns_info = ", ".join(df.columns.tolist())
        stats_summary = df.describe().to_string()
        data_sample = df.head(10).to_string(index=False)
        
        # Generate cache key
        cache_key = get_cache_key(df)
        
        # Check cache
        if 'cache' not in st.session_state:
            st.session_state.cache = {}
        
        # Generate insights with LangGraph
        with st.spinner("Generating insights with Gemini..."):
            try:
                if cache_key in st.session_state.cache:
                    st.info("Using cached results")
                    response = st.session_state.cache[cache_key]
                else:
                    # Use LangGraph to generate insights
                    inputs = {
                        "columns": columns_info,
                        "stats_summary": stats_summary,
                        "data_sample": data_sample
                    }
                    result = app_graph.invoke(inputs)
                    response = result["insights"]
                    # Cache the result
                    st.session_state.cache[cache_key] = response
                
                st.subheader("🔍 AI-Generated Insights")
                st.markdown(response)
                
                # Show cache info and API endpoint
                st.caption(f"Cache key: {cache_key[:8]}...")
                st.info(f"API Endpoint: GET /insights/{cache_key}")
                
            except Exception as e:
                st.error(f"Error generating insights: {str(e)}")
                st.info("Please check your API keys and try again.")
                
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.info("Please make sure the file is properly formatted.")