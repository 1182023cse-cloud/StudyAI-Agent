import requests

pdf_path = r"C:\Users\SAMRUDDHI\Desktop\sanu\Machine_Learning_Notes_2_3_Pages.pdf"

with open(pdf_path, "rb") as pdf_file:

    response = requests.post(
        "http://127.0.0.1:5000/api/upload-pdf",
        files={
            "pdf": pdf_file
        }
    )

print("\n==============================")
print("PDF Upload Response")
print("==============================\n")

print("Status Code:", response.status_code)

print(response.json())