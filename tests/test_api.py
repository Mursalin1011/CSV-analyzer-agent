import requests

# Test the file upload API endpoint
# Make sure the server is running before executing this script

url = "http://127.0.0.1:8000/insights/file"

# Replace 'sample.csv' with the path to your test CSV file
files = {'file': open('..\\sample.csv', 'rb')}

response = requests.post(url, files=files)

if response.status_code == 200:
    data = response.json()
    print("Success!")
    print("Cache Key:", data['cache_key'])
    print("Insights:", data['insights'])
else:
    print("Error:", response.status_code, response.text)