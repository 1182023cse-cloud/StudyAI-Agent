import streamlit as st
import requests


BACKEND_URL = "http://127.0.0.1:5000"


# =================================
# PAGE CONFIGURATION
# =================================

st.set_page_config(
    page_title="StudyAI",
    page_icon="🎓",
    layout="wide"
)


# =================================
# CUSTOM CSS
# =================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: gray;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)


# =================================
# TITLE
# =================================

st.markdown(
    '<div class="main-title">🎓 StudyAI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered College Study Assistant</div>',
    unsafe_allow_html=True
)


# =================================
# SIDEBAR
# =================================

st.sidebar.title("📚 StudyAI Menu")

option = st.sidebar.radio(
    "Select Feature",
    [
        "🏠 Home",
        "🤖 AI Tutor",
        "📄 PDF Q&A",
        "📝 Exam Preparation",
        "📘 Smart Notes",
        "🧠 Flashcards",
        "🧩 Quiz Generator",
        "🎤 Voice Assistant"
    ]
)


# =================================
# HOME
# =================================

if option == "🏠 Home":

    st.header("Welcome to StudyAI 👋")

    st.write(
        "StudyAI is an AI-powered college study assistant "
        "that helps students understand concepts, study PDFs "
        "and prepare for exams."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "🤖 AI Tutor\n\n"
            "Understand difficult concepts easily."
        )

    with col2:
        st.info(
            "📄 PDF Q&A\n\n"
            "Ask questions from your study PDF."
        )

    with col3:
        st.info(
            "📝 Exam Preparation\n\n"
            "Generate important exam questions."
        )

    col4, col5 = st.columns(2)

    with col4:
        st.success(
            "📘 Smart Notes\n\n"
            "Generate structured study notes."
        )

    with col5:
        st.warning(
            "🧠 Flashcards\n\n"
            "Quickly revise important concepts."
        )

    st.info(
        "🧩 Quiz Generator\n\n"
        "Generate 10 MCQs for quick practice."
    )


# =================================
# AI TUTOR
# =================================

elif option == "🤖 AI Tutor":

    st.header("🤖 AI Tutor")

    question = st.text_area(
        "Enter your question",
        placeholder="Example: Explain Machine Learning in simple language."
    )

    mode = st.selectbox(
        "Explanation Mode",
        [
            "simple",
            "example",
            "exam"
        ]
    )

    if st.button("Ask AI Tutor"):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner("AI is thinking..."):

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/api/explain",
                        json={
                            "question": question,
                            "mode": mode
                        }
                    )

                    data = response.json()

                    if response.status_code == 200:

                        st.success("Answer")

                        st.markdown(
                            data["answer"]
                        )

                    else:

                        st.error(
                            data.get(
                                "message",
                                "Something went wrong."
                            )
                        )

                except Exception as e:

                    st.error(
                        f"Backend connection error: {e}"
                    )


# =================================
# PDF Q&A
# =================================

elif option == "📄 PDF Q&A":

    st.header("📄 PDF Based Q&A")

    st.write(
        "Upload your college PDF and ask questions "
        "from the uploaded content."
    )

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        if st.button("Upload PDF"):

            with st.spinner("Uploading PDF..."):

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/api/upload-pdf",
                        files={
                            "pdf": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                "application/pdf"
                            )
                        }
                    )

                    data = response.json()

                    if response.status_code == 200:

                        st.success(
                            "PDF uploaded successfully!"
                        )

                        st.write(
                            f"📄 File: {data['filename']}"
                        )

                        st.write(
                            f"📑 Pages: {data['pages']}"
                        )

                        st.write(
                            f"🧩 Chunks: {data['chunks']}"
                        )

                    else:

                        st.error(
                            data.get(
                                "message",
                                "Upload failed."
                            )
                        )

                except Exception as e:

                    st.error(
                        f"Backend connection error: {e}"
                    )

    st.divider()

    st.subheader("Ask Question from PDF")

    pdf_question = st.text_area(
        "Your question",
        placeholder="Example: What is Machine Learning according to this PDF?"
    )

    if st.button("Ask from PDF"):

        if not pdf_question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner(
                "Searching PDF and generating answer..."
            ):

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/api/ask-pdf",
                        json={
                            "question": pdf_question
                        }
                    )

                    data = response.json()

                    if response.status_code == 200:

                        st.success("Answer")

                        st.markdown(
                            data["answer"]
                        )

                        if "sources" in data:

                            st.subheader("📚 Sources")

                            for source in data["sources"]:

                                st.write(
                                    f"Page {source['page']} "
                                    f"(Score: {source['score']:.3f})"
                                )

                    else:

                        st.error(
                            data.get(
                                "message",
                                "Something went wrong."
                            )
                        )

                except Exception as e:

                    st.error(
                        f"Backend connection error: {e}"
                    )


# =================================
# EXAM PREPARATION
# =================================

elif option == "📝 Exam Preparation":

    st.header("📝 Exam Preparation")

    topic = st.text_input(
        "Enter Topic",
        placeholder="Example: Machine Learning"
    )

    exam_type = st.selectbox(
        "Select Exam Type",
        [
            "important",
            "short",
            "long",
            "mcq",
            "revision"
        ]
    )

    if st.button("Generate Exam Content"):

        if not topic.strip():

            st.warning("Please enter a topic.")

        else:

            with st.spinner(
                "Preparing exam content..."
            ):

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/api/exam",
                        json={
                            "topic": topic,
                            "exam_type": exam_type
                        }
                    )

                    data = response.json()

                    if response.status_code == 200:

                        st.success(
                            "Generated Successfully"
                        )

                        st.markdown(
                            data["answer"]
                        )

                    else:

                        st.error(
                            data.get(
                                "message",
                                "Something went wrong."
                            )
                        )

                except Exception as e:

                    st.error(
                        f"Backend connection error: {e}"
                    )


# =================================
# SMART NOTES
# =================================

elif option == "📘 Smart Notes":

    st.header("📘 Smart Notes Generator")

    topic = st.text_input(
        "Enter Topic",
        placeholder="Example: Artificial Intelligence"
    )

    if st.button("Generate Smart Notes"):

        if not topic.strip():

            st.warning("Please enter a topic.")

        else:

            with st.spinner(
                "Generating notes..."
            ):

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/api/notes",
                        json={
                            "topic": topic
                        }
                    )

                    data = response.json()

                    if response.status_code == 200:

                        st.success(
                            "Notes Generated"
                        )

                        st.markdown(
                            data["notes"]
                        )

                    else:

                        st.error(
                            data.get(
                                "message",
                                "Something went wrong."
                            )
                        )

                except Exception as e:

                    st.error(
                        f"Backend connection error: {e}"
                    )


# =================================
# FLASHCARDS
# =================================

elif option == "🧠 Flashcards":

    st.header("🧠 Flashcard Generator")

    topic = st.text_input(
        "Enter Topic",
        placeholder="Example: Machine Learning"
    )

    if st.button("Generate Flashcards"):

        if not topic.strip():

            st.warning("Please enter a topic.")

        else:

            with st.spinner(
                "Generating flashcards..."
            ):

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/api/flashcards",
                        json={
                            "topic": topic
                        }
                    )

                    data = response.json()

                    if response.status_code == 200:

                        st.success(
                            "Flashcards Generated"
                        )

                        st.markdown(
                            data["flashcards"]
                        )

                    else:

                        st.error(
                            data.get(
                                "message",
                                "Something went wrong."
                            )
                        )

                except Exception as e:

                    st.error(
                        f"Backend connection error: {e}"
                    )


# =================================
# QUIZ GENERATOR
# =================================

elif option == "🧩 Quiz Generator":

    st.header("🧩 AI Quiz Generator")

    st.write(
        "Generate 10 MCQs from any college topic "
        "for quick practice."
    )

    topic = st.text_input(
        "Enter Quiz Topic",
        placeholder="Example: Machine Learning"
    )

    if st.button("Generate Quiz"):

        if not topic.strip():

            st.warning(
                "Please enter a topic."
            )

        else:

            with st.spinner(
                "Generating your quiz..."
            ):

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/api/quiz",
                        json={
                            "topic": topic
                        }
                    )

                    data = response.json()

                    if response.status_code == 200:

                        st.success(
                            "Quiz Generated Successfully!"
                        )

                        st.markdown(
                            data["quiz"]
                        )

                    else:

                        st.error(
                            data.get(
                                "message",
                                "Quiz generation failed."
                            )
                        )

                except Exception as e:

                    st.error(
                        f"Backend connection error: {e}"
                    )


# =================================
# VOICE ASSISTANT
# =================================

elif option == "🎤 Voice Assistant":

    st.header("🎤 StudyAI Voice Assistant")

    st.write(
        "Ask your study question using your voice "
        "and get an AI-generated answer."
    )

    st.components.v1.html(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; padding: 10px; }
                button {
                    padding: 12px 22px;
                    font-size: 17px;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    margin-right: 8px;
                }
                #startButton { background: #4CAF50; color: white; }
                #speakButton { background: #2196F3; color: white; }
                #status { margin-top: 15px; font-weight: bold; }
                #question {
                    margin-top: 15px;
                    padding: 12px;
                    width: 95%;
                    font-size: 16px;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                }
                #answer {
                    margin-top: 15px;
                    padding: 15px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    white-space: pre-wrap;
                    line-height: 1.5;
                }
            </style>
        </head>
        <body>
            <button id="startButton" onclick="startListening()">
                🎤 Start Speaking
            </button>

            <button id="speakButton" onclick="speakAnswer()">
                🔊 Speak Answer
            </button>

            <p id="status">
                Click "Start Speaking" and ask your question.
            </p>

            <input id="question" type="text"
                   placeholder="Your voice question will appear here...">

            <div id="answer">AI answer will appear here.</div>

            <script>
                let currentAnswer = "";

                function startListening() {
                    const SpeechRecognition =
                        window.SpeechRecognition ||
                        window.webkitSpeechRecognition;

                    if (!SpeechRecognition) {
                        document.getElementById("status").innerText =
                            "❌ Speech Recognition is not supported. Please use Google Chrome or Microsoft Edge.";
                        return;
                    }

                    const recognition = new SpeechRecognition();
                    recognition.lang = "en-IN";
                    recognition.interimResults = false;
                    recognition.maxAlternatives = 1;

                    document.getElementById("status").innerText =
                        "🎤 Listening... Please speak now.";

                    recognition.start();

                    recognition.onresult = async function(event) {
                        const transcript =
                            event.results[0][0].transcript;

                        document.getElementById("question").value =
                            transcript;

                        document.getElementById("status").innerText =
                            "⏳ Sending question to StudyAI...";

                        try {
                            const response = await fetch(
                                "http://127.0.0.1:5000/api/ask",
                                {
                                    method: "POST",
                                    headers: {
                                        "Content-Type": "application/json"
                                    },
                                    body: JSON.stringify({
                                        question: transcript
                                    })
                                }
                            );

                            const data = await response.json();

                            if (response.ok) {
                                currentAnswer = data.answer;
                                document.getElementById("answer").innerText =
                                    currentAnswer;

                                document.getElementById("status").innerText =
                                    "✅ Answer generated successfully.";

                                speakAnswer();
                            } else {
                                document.getElementById("answer").innerText =
                                    data.message || "Something went wrong.";

                                document.getElementById("status").innerText =
                                    "❌ Could not generate answer.";
                            }
                        } catch (error) {
                            document.getElementById("status").innerText =
                                "❌ Backend connection error. Make sure backend is running.";

                            document.getElementById("answer").innerText =
                                error;
                        }
                    };

                    recognition.onerror = function(event) {
                        document.getElementById("status").innerText =
                            "❌ Voice error: " + event.error;
                    };
                }

                function speakAnswer() {
                    if (!currentAnswer) {
                        document.getElementById("status").innerText =
                            "⚠️ No answer available to speak.";
                        return;
                    }

                    window.speechSynthesis.cancel();

                    const speech =
                        new SpeechSynthesisUtterance(currentAnswer);

                    speech.lang = "en-IN";
                    speech.rate = 0.9;
                    speech.pitch = 1;

                    window.speechSynthesis.speak(speech);

                    document.getElementById("status").innerText =
                        "🔊 Speaking the answer...";
                }
            </script>
        </body>
        </html>
        """,
        height=450
    )


# =================================
# FOOTER
# =================================

st.sidebar.divider()

st.sidebar.caption(
    "StudyAI 🎓 | AI College Study Assistant"
)