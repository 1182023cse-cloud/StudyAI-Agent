import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from ai_engine import generate_answer
from pdf_processor import extract_pdf_text, create_chunks
from rag_engine import retrieve_relevant_chunks, create_pdf_context


# =================================
# FLASK APP
# =================================

app = Flask(__name__)
CORS(app)


# =================================
# UPLOAD CONFIGURATION
# =================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"pdf"}


# =================================
# PDF MEMORY
# =================================

pdf_chunks = []
uploaded_pdf_name = None


# =================================
# HELPER FUNCTION
# =================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =================================
# HEALTH CHECK
# =================================

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "status": "success",
        "message": "StudyAI Backend is running"
    })


# =================================
# GENERAL AI ASK
# =================================

@app.route("/api/ask", methods=["POST"])
def ask_ai():

    try:

        data = request.get_json()

        question = data.get(
            "question",
            ""
        ).strip()

        if not question:

            return jsonify({
                "status": "error",
                "message": "Question is required"
            }), 400

        answer = generate_answer(question)

        return jsonify({
            "status": "success",
            "question": question,
            "answer": answer
        })

    except Exception as e:

        print("ASK ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# =================================
# PDF UPLOAD
# =================================

@app.route("/api/upload-pdf", methods=["POST"])
def upload_pdf():

    global pdf_chunks
    global uploaded_pdf_name

    try:

        if "pdf" not in request.files:

            return jsonify({
                "status": "error",
                "message": "No PDF file provided"
            }), 400

        file = request.files["pdf"]

        if file.filename == "":

            return jsonify({
                "status": "error",
                "message": "No PDF selected"
            }), 400

        if not allowed_file(file.filename):

            return jsonify({
                "status": "error",
                "message": "Only PDF files are allowed"
            }), 400

        filename = secure_filename(
            file.filename
        )

        file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(file_path)

        pages = extract_pdf_text(
            file_path
        )

        pdf_chunks = create_chunks(
            pages
        )

        uploaded_pdf_name = filename

        total_characters = sum(
            len(page["text"])
            for page in pages
        )

        return jsonify({
            "status": "success",
            "message": "PDF uploaded successfully",
            "filename": filename,
            "pages": len(pages),
            "characters": total_characters,
            "chunks": len(pdf_chunks)
        })

    except Exception as e:

        print("PDF UPLOAD ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# =================================
# PDF QUESTION ANSWERING
# =================================

@app.route("/api/ask-pdf", methods=["POST"])
def ask_pdf():

    try:

        data = request.get_json()

        question = data.get(
            "question",
            ""
        ).strip()

        if not question:

            return jsonify({
                "status": "error",
                "message": "Question is required"
            }), 400

        if not pdf_chunks:

            return jsonify({
                "status": "error",
                "message": "Please upload a PDF first"
            }), 400

        relevant_chunks = retrieve_relevant_chunks(
            pdf_chunks,
            question,
            top_k=4
        )

        context = create_pdf_context(
            relevant_chunks
        )

        prompt = f"""
You are StudyAI, a college PDF study assistant.

Answer the student's question using ONLY
the information provided in the PDF context below.

PDF Context:
{context}

Student Question:
{question}

Instructions:

- Answer clearly and accurately.
- Use simple college-level language.
- Do not invent information.
- If the answer is not available in the PDF,
  clearly say that the information is not
  available in the uploaded PDF.
- Mention the relevant page number when possible.
"""

        answer = generate_answer(
            prompt
        )

        sources = []

        for result in relevant_chunks:

            sources.append({
                "page": result["page"],
                "score": result["score"]
            })

        return jsonify({
            "status": "success",
            "question": question,
            "answer": answer,
            "sources": sources
        })

    except Exception as e:

        print("PDF Q&A ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# =================================
# AI TUTOR
# =================================

@app.route("/api/explain", methods=["POST"])
def explain_topic():

    try:

        data = request.get_json()

        question = data.get(
            "question",
            ""
        ).strip()

        mode = data.get(
            "mode",
            "simple"
        )

        if not question:

            return jsonify({
                "status": "error",
                "message": "Question is required"
            }), 400

        if mode == "simple":

            instruction = """
Explain the concept in very simple
language for a college student.

Include:
- Definition
- Main idea
- Simple explanation
- Example
- Why it is useful
"""

        elif mode == "example":

            instruction = """
Explain the concept using simple
real-world and technical examples.

Include:
- Definition
- Main concept
- Real-world example
- Technical example
"""

        elif mode == "exam":

            instruction = """
Explain the concept from an exam
preparation point of view.

Include:
- Definition
- Key points
- Important concepts
- Example
- Exam-focused answer
"""

        else:

            instruction = """
Explain the concept clearly and simply.
"""

        prompt = f"""
You are StudyAI, an AI college tutor.

Student Question:
{question}

{instruction}

Requirements:

- Use simple college-level language.
- Use clear headings.
- Use bullet points where useful.
- Do not add unrelated information.
"""

        answer = generate_answer(
            prompt
        )

        return jsonify({
            "status": "success",
            "question": question,
            "mode": mode,
            "answer": answer
        })

    except Exception as e:

        print("AI TUTOR ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# =================================
# EXAM PREPARATION
# =================================

@app.route("/api/exam", methods=["POST"])
def exam_preparation():

    try:

        data = request.get_json()

        topic = data.get(
            "topic",
            ""
        ).strip()

        exam_type = data.get(
            "exam_type",
            "important"
        )

        if not topic:

            return jsonify({
                "status": "error",
                "message": "Topic is required"
            }), 400

        if exam_type == "important":

            prompt = f"""
You are StudyAI, an AI college exam
preparation assistant.

Topic:
{topic}

Create important exam questions.

Generate:

Part A:
5 short-answer questions.

Part B:
5 long-answer questions.

Requirements:

- Questions must be academically relevant.
- Cover important concepts.
- Use simple language.
- Do not repeat questions.
"""

        elif exam_type == "short":

            prompt = f"""
Generate 10 important short-answer
exam questions for:

{topic}

Requirements:

- College-level questions.
- Cover different concepts.
- Keep questions clear.
- Do not repeat questions.
"""

        elif exam_type == "long":

            prompt = f"""
Generate 10 important long-answer
exam questions for:

{topic}

Requirements:

- College-level questions.
- Cover major concepts.
- Suitable for university exams.
- Do not repeat questions.
"""

        elif exam_type == "mcq":

            prompt = f"""
You are StudyAI, a college exam quiz
generator.

Create EXACTLY 10 academic MCQs
about:

{topic}

For every question provide:

Question:
[Question]

A) [Option]
B) [Option]
C) [Option]
D) [Option]

Correct Answer:
[Correct option]

Explanation:
[Short explanation]

Requirements:

- EXACTLY 10 questions.
- Exactly 4 options per question.
- One correct answer.
- Include explanations.
- Questions must be academic.
- Questions must be related only to the topic.
- Do not repeat questions.
- Do not output JSON.
- Do not include safety classifications.
"""

        elif exam_type == "revision":

            prompt = f"""
Create a quick revision guide for:

{topic}

Include:

1. Important definitions
2. Important concepts
3. Key points
4. Important formulas if applicable
5. Important examples
6. Frequently asked concepts
7. Last-minute revision points

Use simple language.
"""

        else:

            prompt = f"""
Create useful exam preparation
material for:

{topic}

Include important questions,
key concepts and revision points.
"""

        answer = generate_answer(
            prompt
        )

        return jsonify({
            "status": "success",
            "topic": topic,
            "exam_type": exam_type,
            "answer": answer
        })

    except Exception as e:

        print("EXAM ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# =================================
# SMART NOTES
# =================================

@app.route("/api/notes", methods=["POST"])
def smart_notes():

    try:

        data = request.get_json()

        topic = data.get(
            "topic",
            ""
        ).strip()

        if not topic:

            return jsonify({
                "status": "error",
                "message": "Topic is required"
            }), 400

        prompt = f"""
You are StudyAI, an AI college
Smart Notes Generator.

Create clear and useful study notes
for the following college topic:

Topic:
{topic}

Include:

1. Definition
2. Key Concepts
3. Important Points
4. Types or Categories
5. Simple Examples
6. Advantages
7. Disadvantages
8. Applications
9. Exam Important Points
10. Quick Revision Summary

Requirements:

- Use simple college-level language.
- Use clear headings.
- Use bullet points where suitable.
- Keep the explanation easy to understand.
- Focus only on the given topic.
- Make the notes useful for exam preparation.
- Do not add unrelated information.
"""

        answer = generate_answer(
            prompt
        )

        return jsonify({
            "status": "success",
            "topic": topic,
            "notes": answer
        })

    except Exception as e:

        print("NOTES ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# =================================
# FLASHCARDS
# =================================

@app.route("/api/flashcards", methods=["POST"])
def flashcards():

    try:

        data = request.get_json()

        topic = data.get(
            "topic",
            ""
        ).strip()

        if not topic:

            return jsonify({
                "status": "error",
                "message": "Topic is required"
            }), 400

        prompt = f"""
You are StudyAI, an AI college
Flashcard Generator.

Create exactly 10 useful study
flashcards for the following topic:

Topic:
{topic}

For every flashcard use this format:

Flashcard 1:
Question: [Write a clear academic question]
Answer: [Give a short and accurate answer]

Flashcard 2:
Question: [Write a clear academic question]
Answer: [Give a short and accurate answer]

Continue until Flashcard 10.

Requirements:

- Create EXACTLY 10 flashcards.
- Questions must be related to the given topic.
- Use college-level academic concepts.
- Answers should be short and easy to remember.
- Cover different important concepts.
- Do not repeat the same question.
- Use simple language.
- Do not output JSON.
- Do not add unrelated information.
"""

        answer = generate_answer(
            prompt
        )

        return jsonify({
            "status": "success",
            "topic": topic,
            "flashcards": answer
        })

    except Exception as e:

        print("FLASHCARDS ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# =================================
# QUIZ GENERATOR
# =================================

@app.route("/api/quiz", methods=["POST"])
def quiz_generator():

    try:

        data = request.get_json()

        topic = data.get(
            "topic",
            ""
        ).strip()

        if not topic:

            return jsonify({
                "status": "error",
                "message": "Topic is required"
            }), 400

        prompt = f"""
You are StudyAI, an AI college quiz generator.

Create a quiz on the following topic:

Topic:
{topic}

Requirements:

- Create EXACTLY 10 multiple-choice questions.
- Each question must have exactly 4 options.
- Every question must have only one correct answer.
- Clearly mention the correct answer.
- Give a short explanation for every answer.
- Cover different important concepts from the topic.
- Use college-level academic content.
- Use simple and easy-to-understand language.
- Do not repeat questions.
- Do not create questions unrelated to the topic.
- Do not output JSON.

Use exactly this format:

Question 1:
[Question]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

Correct Answer:
[Correct option]

Explanation:
[Short explanation]

Question 2:
[Question]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

Correct Answer:
[Correct option]

Explanation:
[Short explanation]

Continue the same format until Question 10.
"""

        answer = generate_answer(
            prompt
        )

        return jsonify({
            "status": "success",
            "topic": topic,
            "quiz": answer
        })

    except Exception as e:

        print("QUIZ ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# =================================
# RUN FLASK SERVER
# =================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )