from typing import Dict, Any
from langchain.callbacks import tracing_v2_enabled
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from csv_analyzer.models.llm import get_llm, INSIGHTS_PROMPT
from csv_analyzer.cache.cache_manager import CacheManager

# Define state for LangGraph
class AnalysisState(TypedDict):
    data_sample: str
    columns: str
    stats_summary: str
    insights: Annotated[str, operator.add]

class DataAnalyzer:
    """Main class for analyzing data and generating insights"""
    
    def __init__(self):
        self.llm = get_llm()
        self.cache_manager = CacheManager()
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow for analysis"""
        def generate_insights(state: AnalysisState) -> Dict[str, Any]:
            """Generate insights using LLM"""
            with tracing_v2_enabled():
                try:
                    chain = INSIGHTS_PROMPT | self.llm
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
        
        return workflow.compile()
    
    def analyze(self, data_info: Dict[str, str]) -> str:
        """Analyze data and return insights"""
        # Generate insights with LangGraph
        inputs = {
            "columns": data_info["columns"],
            "stats_summary": data_info["stats_summary"],
            "data_sample": data_info["data_sample"]
        }
        result = self.workflow.invoke(inputs)
        return result["insights"]
    
    def analyze_with_caching(self, data_info: Dict[str, str], cache_key: str) -> str:
        """Analyze data with caching support"""
        # Try to load from cache first
        cached_insights = self.cache_manager.load_insights(cache_key)
        if cached_insights:
            return cached_insights
        
        # Generate new insights
        insights = self.analyze(data_info)
        
        # Save to cache
        self.cache_manager.save_insights(cache_key, insights)
        
        return insights