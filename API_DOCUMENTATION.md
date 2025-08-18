# CSV Insights API Documentation

This document provides detailed information about the CSV Insights API endpoints, request/response formats, and usage examples.

## Base URL

```
http://localhost:8000
```

When running on your local network, you can also access it via:
```
http://YOUR_LOCAL_IP:8000
```

## API Endpoints

### 1. Health Check

**GET** `/health`

Check if the API is running and healthy.

#### Response
```json
{
  "status": "healthy",
  "llm_provider": "gemini"  // or "ollama"
}
```

### 2. Upload File and Get Insights

**POST** `/insights/file`

Upload a CSV, Excel (XLSX/XLS), or JSON file to generate AI-powered insights.

#### Request

**Form Data:**
- `file`: The file to analyze (CSV, XLSX, XLS, or JSON)

#### Response

```json
{
  "insights": "string",  // AI-generated insights in markdown format
  "cache_key": "string"  // Unique identifier for caching
}
```

#### Example Response

```json
{
  "insights": "### Dataset Analysis\\n\\n#### Key Patterns/Trends\\n- The dataset contains 1000 entries with 5 columns\\n- Age distribution is fairly uniform between 20-60 years\\n- Salary shows a positive correlation with experience\\n\\n#### Notable Correlations/Anomalies\\n- Strong positive correlation (0.78) between years_of_experience and salary\\n- Outliers detected in the salary column (3 entries above 2 standard deviations)\\n\\n#### Business Implications\\n- The data suggests a consistent compensation structure\\n- Consider investigating the salary outliers for potential discrepancies\\n\\n#### Analysis Recommendations\\n- Perform a deeper regression analysis on salary predictors\\n- Segment analysis by department for more granular insights",
  "cache_key": "a1b2c3d4e5f67890"
}
```

### 3. Get Insights by Cache Key

**GET** `/insights/{cache_key}`

Retrieve previously generated insights using the cache key.

#### Request

**Path Parameters:**
- `cache_key`: The unique identifier returned from file upload

#### Response

```json
{
  "insights": "string",  // AI-generated insights in markdown format
  "cache_key": "string"  // The cache key used for retrieval
}
```

#### Error Response

If the cache key is not found:
```json
{
  "detail": "Insights not found for this key"
}
```

### 4. Get All Insights

**GET** `/insights`

Retrieve all previously generated insights with their cache keys.

#### Response

```json
{
  "insights": [
    {
      "cache_key": "string",
      "insights": "string"
    }
  ]
}
```

### 5. Search Insights

**GET** `/insights/search/{query}`

Search through all insights for a specific query term.

#### Request

**Path Parameters:**
- `query`: The search term to look for in insights

#### Response

```json
{
  "results": [
    {
      "cache_key": "string",
      "insights": "string"
    }
  ],
  "count": "integer"
}
```

## Supported File Formats

- **CSV** (.csv)
- **Excel** (.xlsx, .xls)
- **JSON** (.json)

## Usage Examples

### cURL Examples

#### Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

#### Upload File
```bash
curl -X POST "http://localhost:8000/insights/file" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_data.csv"
```

#### Get Insights by Cache Key
```bash
curl -X GET "http://localhost:8000/insights/a1b2c3d4e5f67890"
```

#### Get All Insights
```bash
curl -X GET "http://localhost:8000/insights"
```

#### Search Insights
```bash
curl -X GET "http://localhost:8000/insights/search/phone"
```

### Python Example

```python
import requests

# Upload file and get insights
with open('sample_data.csv', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/insights/file', files=files)
    result = response.json()
    print("Insights:", result['insights'])
    print("Cache Key:", result['cache_key'])

# Retrieve insights by cache key
cache_key = result['cache_key']
response = requests.get(f'http://localhost:8000/insights/{cache_key}')
insights = response.json()
print("Cached Insights:", insights['insights'])

# Get all insights
response = requests.get('http://localhost:8000/insights')
all_insights = response.json()
print("All Insights:", all_insights)

# Search insights
response = requests.get('http://localhost:8000/insights/search/phone')
search_results = response.json()
print("Search Results:", search_results)
```

## Error Handling

The API returns standard HTTP status codes:

- **200**: Success
- **400**: Bad Request (e.g., unsupported file format)
- **404**: Not Found (e.g., cache key not found)
- **500**: Internal Server Error (e.g., processing error)

## Caching

Results are cached in a SQLite database to avoid reprocessing the same file. The cache key is generated based on a sample of the data, so identical files will return the same cache key and retrieve cached results.

## LLM Providers

The API supports two LLM providers:

1. **Google Gemini** (default) - Requires API key
2. **Ollama** (local) - Requires Ollama running locally

Switch between providers using environment variables:
```
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_api_key_here

# Or for Ollama:
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:0.6b
```

## Accessing Swagger UI

Once the API is running, you can access the interactive Swagger documentation at:
```
http://localhost:8000/docs
```

This provides an interactive interface to test all API endpoints directly from your browser.