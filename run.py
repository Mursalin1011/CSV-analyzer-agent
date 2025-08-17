import subprocess
import uvicorn
import sys
import os
import socket

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Connect to a remote server to determine local IP
        # This doesn't actually send any data
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        # Fallback to localhost if unable to determine local IP
        return "127.0.0.1"

def run_streamlit():
    # Run Streamlit as a separate process
    cmd = [sys.executable, "-m", "streamlit", "run", "trial1.py", "--server.port=8501"]
    subprocess.Popen(cmd)

def run_api():
    # Import the API app inside the function to avoid circular imports
    from api import api_app
    
    # Get local IP for displaying to user
    local_ip = get_local_ip()
    
    # Print accessible addresses
    print("=" * 50)
    print("CSV Analyzer Agent is running!")
    print("=" * 50)
    print(f"FastAPI (Local only):   http://127.0.0.1:8000")
    print(f"FastAPI Docs (Swagger): http://127.0.0.1:8000/docs")
    print(f"FastAPI (Network):      http://{local_ip}:8000")
    print(f"Streamlit UI:           http://127.0.0.1:8501")
    print("=" * 50)
    print("Press Ctrl+C to stop the servers")
    print("=" * 50)
    
    # Run on all interfaces to make it accessible on the local network
    uvicorn.run(api_app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Run Streamlit in a separate process
    run_streamlit()
    
    # Run FastAPI server
    run_api()