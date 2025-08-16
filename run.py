import subprocess
import uvicorn
import sys
import os
from api import api_app

def run_streamlit():
    # Run Streamlit as a separate process
    cmd = [sys.executable, "-m", "streamlit", "run", "trial1.py", "--server.port=8501"]
    subprocess.Popen(cmd)

def run_api():
    uvicorn.run(api_app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    # Run Streamlit in a separate process
    run_streamlit()
    
    # Run FastAPI server
    run_api()