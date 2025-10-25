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
    git clone https://github.com/your-username/pdf-chatbot.git
    cd pdf-chatbot
- 2️⃣ Build the Docker image
    docker compose build
- 3️⃣ Run the chatbot
    docker compose up
  
## ⚙️ Configuration
 - You can adjust default settings in the .env file:
   
               STREAMLIT_SERVER_PORT=8501
   
## 🧩 How It Works

- Upload a PDF or TXT file
   - The system extracts and splits text into manageable chunks.
   - Each chunk is embedded using a local transformer model.
   - A FAISS index stores embeddings for efficient search.
   - When you ask a question:
        - Relevant chunks are retrieved.
        - The local LLM model generates an answer from context.

## 📜 License
   This project is released under the MIT License.
   
   You are free to use, modify, and distribute it with attribution.
 
## 👨‍💻 Author
Randhir Kumar

📧randhirkumar015@gmail.com

💼 AI/ML & Data Science Enthusiast
