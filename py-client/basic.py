import requests

endpoint = "https://httpbin.org/anything"

get_response = requests.get(endpoint, json={"query": "Hello Word"})

print(get_response.json())