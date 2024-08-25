import requests
import json

url = "http://localhost:8080/v1/chat/completions"
payload = {
    "model": "meta-llama-3.1-8b-instruct",
    "messages": [{"role": "user", "content": "Hello, LocalAI!"}],
    "temperature": 0.7  
}
headers = {"Authorization": "Bearer localai"}  # replace with your API key

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    response_data = response.json()
    print(response_data)
    # process the response data
else:
    print(f"Request failed with status {response.status_code}")
