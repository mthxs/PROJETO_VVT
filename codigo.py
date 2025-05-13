import os
import requests

api_url = os.getenv("API_URL")
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
environment = os.getenv("ENVIRONMENT")

headers = {
    "Authorization": f"Bearer {api_key}:{api_secret}",
    "Content-Type": "application/json"
}

payload = {
    "env": environment,
    "message": "Hello from GitHub Actions!"
}

response = requests.post(api_url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response: ", response.text)
