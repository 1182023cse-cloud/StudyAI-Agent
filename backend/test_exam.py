import requests

response = requests.post(
    "http://127.0.0.1:5000/api/exam",
    json={
        "topic": "Machine Learning",
        "exam_type": "mcq"
    }
)

print("\n==============================")
print("Exam Preparation Response")
print("==============================\n")

print("Status Code:", response.status_code)

print(response.json())