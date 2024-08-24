import os
import requests


url = "http://localhost:8080/v1/completions"
data = {
    "prompt": "Tell me a short joke",
    "model": "mistral-7b-instruct-v0.3",
    "max_tokens": 60,
    "n": 1,
    "stop": None,
    "temperature": 0.9,
}

response = requests.post(url, json=data)
print(response.json()["choices"][0]["text"])
