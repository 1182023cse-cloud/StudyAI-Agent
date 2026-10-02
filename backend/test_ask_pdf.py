import requests


response = requests.post(
    "http://127.0.0.1:5000/api/ask-pdf",
    json={
        "question": "What is Machine Learning?"
    }
)


print("\n==============================")
print("PDF Question Answer")
print("==============================\n")

print("Status Code:", response.status_code)

print(response.json())