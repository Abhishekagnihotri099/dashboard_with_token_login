import requests

# Endpoint URL
url = "http://127.0.0.1:8000/generate-token"

# Sending POST request
response = requests.post(url)

# Print the response
if response.status_code == 200:
    print("Token:", response.json()["token"])
else:
    print("Error:", response.status_code, response.text)

# curl -X POST http://127.0.0.1:8000/generate-token
# https://ddkia4xzi9lav4ttq8xwdz.streamlit.app/?token=GENERATED_TOKEN
