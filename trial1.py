# requirements.txt
# langchain-google-genai
# pandas
# python-dotenv
# streamlit
# openpyxl
# langsmith
# langgraph

import os
import hashlib
import pandas as pd
import streamlit as st
from io import StringIO, BytesIO
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.callbacks import tracing_v2_enabled
from langchain_community.cache import InMemoryCache
from langchain.globals import set_llm_cache
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
import requests
from utils import save_insights_to_file


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
    temperature=0.1  # Reduced from 0.3 for more focused responses
)

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
    # Use a smaller sample for cache key to reduce computation
    sample = df.head(3).to_string(index=False)  # Reduced from 10 to 3 rows
    return hashlib.md5(sample.encode()).hexdigest()

# Streamlit UI
st.title("📊 CSV Data Insights Generator")
st.markdown("Upload your data file to get AI-powered insights using Google Gemini")

# Display API information
st.info("API Endpoint for file upload: POST http://127.0.0.1:8000/insights/file")

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
        # Limit stats to essential metrics to reduce token usage
        stats_summary = df.describe().loc[['count', 'mean', 'std']].to_string()  # Only key stats
        # Limit data sample to reduce token usage
        data_sample = df.head(5).to_string(index=False)  # Reduced from 10 to 5 rows
        
        # Generate cache key
        cache_key = get_cache_key(df)
        
        # Generate insights with LangGraph
        with st.spinner("Generating insights with Gemini..."):
            try:
                # Use LangGraph to generate insights
                inputs = {
                    "columns": columns_info,
                    "stats_summary": stats_summary,
                    "data_sample": data_sample
                }
                result = app_graph.invoke(inputs)
                response = result["insights"]
                
                # Save insights to file
                save_insights_to_file(cache_key, response)
                
                st.subheader("🔍 AI-Generated Insights")
                st.markdown(response)
                
                # Show cache info and API endpoint
                st.caption(f"Cache key: {cache_key[:8]}...")
                st.info(f"GET API Endpoint: http://127.0.0.1:8000/insights/{cache_key}")
                st.info(f"POST API Endpoint: POST http://127.0.0.1:8000/insights/file (upload file to get insights)")
                
            except Exception as e:
                st.error(f"Error generating insights: {str(e)}")
                st.info("Please check your API keys and try again.")
                
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.info("Please make sure the file is properly formatted.")