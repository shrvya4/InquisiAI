# 🧠 InquisiAI – AI-Powered Summarizer for Research Papers & YouTube Videos

InquisiAI is an intelligent assistant built using the **Gemini AI API** that summarizes complex research papers and long YouTube videos into concise, readable insights. Designed for students, researchers, content creators, and curious minds, InquisiAI turns overwhelming content into bite-sized takeaways in seconds.

---

## 🚀 Features

- 📄 **Research Paper Summarization**  
  Input any academic article or PDF (via URL or content) and receive a structured summary with highlights and conclusions.

- 🎥 **YouTube Video Summarization**  
  Paste a YouTube video link to get:
  - A summary of the video content
  - Key points with timestamps
  - Extracted keywords/topics

- 🧠 **Powered by Gemini AI**  
  Utilizes **Gemini API’s function calling** and advanced language modeling for intelligent text understanding and summarization.

- ✨ **Clean and Interactive Output**  
  Clear, easy-to-read results that can be used for quick learning, citations, or content planning.

---

## 🛠️ Technologies Used

- **Gemini AI API** – For language understanding and summarization
- **Python** – Core scripting and backend logic
- **FastAPI** – API backend for serving requests
- **LangChain (Optional)** – For chaining summarization tasks or handling multiple document inputs
- **YouTube Transcript API** – To fetch video transcripts
- **PyMuPDF / PDFPlumber** – For research paper parsing (PDF)

---

## 📦 Installation

### Backend Setup

```bash
git clone https://github.com/your-username/inquisiAI.git
cd inquisiAI/backend
pip install -r requirements.txt
