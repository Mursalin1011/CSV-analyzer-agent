from csv_analyzer.api.main import api_app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api_app, host="127.0.0.1", port=8000)