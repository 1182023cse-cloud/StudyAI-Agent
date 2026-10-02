import requests


response = requests.post(
    "http://127.0.0.1:5000/api/notes",
    json={
        "topic": "Machine Learning"
    }
)


print("\n==============================")
print("Smart Notes Response")
print("==============================\n")

print("Status Code:", response.status_code)

print(response.json())
