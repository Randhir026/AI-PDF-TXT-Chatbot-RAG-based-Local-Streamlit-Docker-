# AI-PDF-TXT-Chatbot-RAG-based-Local-Streamlit-Docker-
This project is a Retrieval-Augmented Generation (RAG) based chatbot that lets you upload PDF or TXT documents and ask questions about their content — all running locally (⚡ no API keys or internet dependency required after setup).

---

## 🚀 Features

- 📂 Upload **PDF or TXT** documents
- 🧠 Automatically chunk and embed text
- 🔎 Retrieve most relevant content using **FAISS**
- 💬 Generate answers locally using **open-source models**
- ⚙️ Fully **offline** — no OpenAI or external API required
- 🖥️ Clean and responsive **Streamlit UI**

---

## 📁 Folder Structure
pdf-chatbot/
│
├── app/
│   ├── main.py                     ← Streamlit app (UI)
│   └── src/
│       ├── embedding_utils.py      ← Embeddings + FAISS
│       ├── generator.py            ← Local generator (DistilGPT2)
│       └── pdf_utils.py            ← PDF text chunking
│
├── chunks/                         ← Stores document chunks
├── vectordb/                       ← Stores FAISS index
│
├── requirements.txt                ← Python dependencies
├── Dockerfile                      ← Build environment
├── docker-compose.yml              ← Run services
├── .env                            ← Environment config (port)
└── README.md


## 🚀 How to Run (Step-by-Step)
 - 1️⃣ Clone the repository
