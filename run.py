import threading
import uvicorn
from trial1 import api_app  # Replace with actual filename

def run_streamlit():
    import streamlit.web.bootstrap
    streamlit.web.bootstrap.run('trial1.py', '', [], {})  # Replace with actual filename

def run_api():
    uvicorn.run(api_app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    # Run Streamlit in a separate thread
    st_thread = threading.Thread(target=run_streamlit)
    st_thread.start()
    
    # Run FastAPI server
    run_api()