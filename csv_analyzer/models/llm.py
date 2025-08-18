from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from typing import Any, Union
from csv_analyzer.core.config import Config

def get_llm() -> Union[ChatGoogleGenerativeAI, OllamaLLM]:
    """Initialize and return the appropriate LLM based on configuration"""
    if Config.LLM_PROVIDER == "gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0.1
        )
    elif Config.LLM_PROVIDER == "ollama":
        return OllamaLLM(
            model=Config.OLLAMA_MODEL,
            base_url=Config.OLLAMA_BASE_URL,
            temperature=0.1
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {Config.LLLM_PROVIDER}")

# Prompt template for data insights
INSIGHTS_PROMPT = PromptTemplate(
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
    5. Add a confidence score (0-100) for each insight
    
    Format in clear markdown with headers.
    """
)