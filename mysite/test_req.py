import requests

r = requests.get("http://127.0.0.1:8000/")
result = r.json()
print(result)


r = requests.get("http://127.0.0.1:8000/add_one")
result = r.json()
print(result)
