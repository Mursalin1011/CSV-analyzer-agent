# Script to run only the API server for testing Swagger docs
import uvicorn
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

if __name__ == "__main__":
    from api import api_app
    
    local_ip = get_local_ip()
    
    print("=" * 60)
    print("CSV Insights API - Documentation Testing")
    print("=" * 60)
    print(f"FastAPI Documentation (Swagger UI): http://127.0.0.1:8000/docs")
    print(f"FastAPI Documentation (ReDoc):      http://127.0.0.1:8000/redoc")
    print(f"API Base URL (Local):               http://127.0.0.1:8000")
    print(f"API Base URL (Network):             http://{local_ip}:8000")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Run on all interfaces to make it accessible on the local network
    uvicorn.run(api_app, host="0.0.0.0", port=8000)