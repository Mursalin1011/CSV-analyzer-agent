"""
Streamlit UI for CSV Analyzer Agent
"""
import streamlit as st
import pandas as pd
import requests
import os
import sys
from io import StringIO, BytesIO

# Add the current directory to the Python path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from csv_analyzer.core.config import Config
    from csv_analyzer.core.data_processor import load_data, get_dataset_info, generate_cache_key
    from csv_analyzer.core.analyzer import DataAnalyzer
except ImportError:
    # Fallback to relative imports if the above fails
    from ..core.config import Config
    from ..core.data_processor import load_data, get_dataset_info, generate_cache_key
    from ..core.analyzer import DataAnalyzer

def main():
    # Initialize configuration
    try:
        config_valid, config_error = Config.validate()
        if not config_valid:
            st.error(f"Configuration error: {config_error}")
            st.stop()
    except Exception as e:
        st.error(f"Error initializing configuration: {e}")
        st.stop()

    # Initialize analyzer
    try:
        analyzer = DataAnalyzer()
    except Exception as e:
        st.error(f"Error initializing analyzer: {e}")
        st.stop()

    # Initialize session state for chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "cache_keys" not in st.session_state:
        st.session_state.cache_keys = []

    # Streamlit UI
    st.title(Config.APP_TITLE)
    st.markdown(f"Upload your data file to get AI-powered insights using {Config.LLM_PROVIDER.upper()}")

    # Create tabs for file upload and chat
    # tab1, tab2 = st.tabs(["File Upload", "Chat with Insights"])
    tab1 = st.tabs(["File Upload"])[0]


    with tab1:
        # Display API information
        st.info("API Endpoint for file upload: POST http://127.0.0.1:8000/insights/file")

        # File uploader with multiple format support
        uploaded_file = st.file_uploader(
            "Upload your file", 
            type=["csv", "xlsx", "xls", "json"]
        )

        # Process the uploaded file
        if uploaded_file:
            try:
                # Determine file extension
                file_extension = uploaded_file.name.split('.')[-1].lower()
                
                # Read file content
                if file_extension in ['csv']:
                    content = uploaded_file.getvalue().decode('utf-8')
                    df = load_data(content, file_extension)
                else:
                    content = uploaded_file.getvalue()
                    df = load_data(content, file_extension)
                
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
                
                # Get dataset info
                data_info = get_dataset_info(df)
                
                # Generate cache key
                cache_key = generate_cache_key(df)
                
                # Generate insights with caching
                with st.spinner(f"Generating insights with {Config.LLM_PROVIDER.upper()}..."):
                    try:
                        insights = analyzer.analyze_with_caching(data_info, cache_key)
                        
                        # Add cache key to session state
                        if cache_key not in st.session_state.cache_keys:
                            st.session_state.cache_keys.append(cache_key)
                        
                        st.subheader("🔍 AI-Generated Insights")
                        st.markdown(insights)
                        
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

    # Chat interface in tab2
    # with tab2:
    #     st.header("💬 Chat with Insights")
    #     st.markdown("Ask questions about your data insights. The AI will retrieve relevant information from previously analyzed datasets.")
        
    #     # Display available cache keys
    #     if st.session_state.cache_keys:
    #         st.subheader("Available Datasets")
    #         for key in st.session_state.cache_keys:
    #             st.code(f"Cache Key: {key[:8]}...", language="text")
    #     else:
    #         st.info("No datasets available yet. Please upload a file in the 'File Upload' tab first.")
        
    #     # Display chat messages
    #     for message in st.session_state.messages:
    #         with st.chat_message(message["role"]):
    #             st.markdown(message["content"])
        
    #     # Chat input
    #     if prompt := st.chat_input("Ask about your data insights..."):
    #         # Add user message to chat history
    #         st.session_state.messages.append({"role": "user", "content": prompt})
    #         with st.chat_message("user"):
    #             st.markdown(prompt)
            
    #         # Process the user's request
    #         with st.chat_message("assistant"):
    #             message_placeholder = st.empty()
    #             full_response = ""
                
    #             # Check if user is asking for a specific insight by cache key
    #             if "cache key" in prompt.lower() or "cache_key" in prompt.lower():
    #                 # Extract cache key from prompt (simple approach)
    #                 cache_key = None
    #                 for key in st.session_state.cache_keys:
    #                     if key[:8] in prompt:
    #                         cache_key = key
    #                         break
                    
    #                 if cache_key:
    #                     try:
    #                         # Call the API to get insights
    #                         api_url = f"http://127.0.0.1:8000/insights/{cache_key}"
    #                         response = requests.get(api_url)
                            
    #                         if response.status_code == 200:
    #                             insights_data = response.json()
    #                             full_response = f"Here are the insights for cache key {cache_key[:8]}...:\n\n{insights_data['insights']}"
    #                         else:
    #                             full_response = f"Sorry, I couldn't retrieve insights for that cache key. Error: {response.status_code}"
    #                     except Exception as e:
    #                         full_response = f"Sorry, I encountered an error while retrieving insights: {str(e)}"
    #                 else:
    #                     full_response = "Please specify a valid cache key. You can find available cache keys above."
    #             else:
    #                 # For general questions, we could implement a more sophisticated approach
    #                 # For now, we'll just provide instructions
    #                 full_response = "I can help you retrieve insights from your analyzed datasets. Please specify which dataset you're interested in by mentioning its cache key. You can find the available cache keys listed above."
                
    #             message_placeholder.markdown(full_response)
            
    #         # Add assistant response to chat history
    #         st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()