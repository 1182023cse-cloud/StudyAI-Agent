import requests


response = requests.post(
    "http://127.0.0.1:5000/api/explain",
    json={
        "question": "What is Machine Learning?",
        "mode": "simple"
    }
)


print("\n==============================")
print("AI Tutor Response")
print("==============================\n")

print("Status Code:", response.status_code)

print(response.json())