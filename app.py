import os
import json
import fitz  # PyMuPDF
import re
from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure Google Gemini API
genai.configure(api_key="")  # Replace with your actual API key

chat_model = genai.GenerativeModel("gemini-1.5-pro")
chat_session = None
loaded_text = ""

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = " ".join(page.get_text() for page in doc)
    return text.strip()

def extract_text_from_youtube(url):
    try:
        video_id = url.split("v=")[-1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([item['text'] for item in transcript])
    except Exception as e:
        return f"Error: {e}"

def summarize_text(text):
    prompt = f"""
You are a summarizer and evaluator.

Given the following content:
\"\"\"{text}\"\"\"

Return a JSON object with:
1. summary: A short summary
2. key_points: Bullet list
3. evaluation: Rate clarity from 1-10
4. linkedin_post: Create a professional LinkedIn post about the content

ONLY return valid JSON.
"""
    response = chat_model.generate_content(prompt)
    try:
        json_str = re.search(r'\{.*\}', response.text, re.DOTALL).group(0)
        return json.loads(json_str)
    except Exception:
        return {"summary": "Error parsing Gemini response", "raw": response.text}

@app.route("/", methods=["GET", "POST"])
def index():
    global loaded_text, chat_session
    summary = {}
    if request.method == "POST":
        file = request.files.get("pdf")
        url = request.form.get("youtube_url")

        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            loaded_text = extract_text_from_pdf(filepath)
        elif url:
            loaded_text = extract_text_from_youtube(url)

        if loaded_text:
            chat_session = chat_model.start_chat()
            summary = summarize_text(loaded_text)

    return render_template("index.html", summary=summary)

@app.route("/ask", methods=["POST"])
def ask():
    global chat_session, loaded_text
    question = request.json.get("question", "")

    if not chat_session or not loaded_text:
        return jsonify({"answer": "Please upload a PDF or enter a YouTube link first."})

    chat_session.send_message(f"Use this context:\n\n{loaded_text}")
    response = chat_session.send_message(question)
    return jsonify({"answer": response.text})

if __name__ == "__main__":
    app.run(debug=True)
