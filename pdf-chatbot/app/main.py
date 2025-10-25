import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import streamlit as st
import os
import pickle
import fitz  # PyMuPDF

from src.embedding_utils import Embedder
from src.generator import Generator
from src.pdf_utils import chunk_text  # keep your existing chunk_text function

# -----------------------------
# Helper function: Extract text from PDF
# -----------------------------
def extract_text_from_pdf(file):
    """
    Accepts either:
    - file path (str)
    - file-like object (BytesIO from Streamlit upload)
    """
    text = ""
    if not isinstance(file, str):
        # Streamlit uploaded file
        file.seek(0)
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
        pdf.close()
    else:
        # Regular file path
        with fitz.open(file) as pdf:
            for page in pdf:
                text += page.get_text()
    return text

# -----------------------------
# Paths for storing chunks & FAISS index
# -----------------------------
CHUNK_DIR = "chunks"
INDEX_DIR = "vectordb"
CHUNK_PATH = os.path.join(CHUNK_DIR, "document_chunks.pkl")
INDEX_PATH = os.path.join(INDEX_DIR, "document_index.faiss")

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="📘 AI PDF/TXT Chatbot", layout="wide")
st.title("🤖 Ask Your Document Anything")
st.markdown(
    "Upload a PDF or TXT file and ask questions using retrieval-augmented generation (RAG)."
)

# Sidebar: Upload document
st.sidebar.header("📂 Upload Document")
uploaded_file = st.sidebar.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

# -----------------------------
# Load Data
# -----------------------------
@st.cache_resource
def load_data(file):
    """Process uploaded file: extract text, chunk, generate/load embeddings & FAISS index"""
    if file is None:
        return None, None

    os.makedirs(CHUNK_DIR, exist_ok=True)
    os.makedirs(INDEX_DIR, exist_ok=True)

    # Extract text
    if file.type == "application/pdf":
        text = extract_text_from_pdf(file)
    else:  # TXT file
        file.seek(0)
        text = file.read().decode("utf-8")

    # Chunk text
    chunks = chunk_text(text)
    with open(CHUNK_PATH, "wb") as f:
        pickle.dump(chunks, f)

    # Embeddings
    embedder = Embedder()
    index_loaded = embedder.load_index(INDEX_PATH)
    if not index_loaded or embedder.index.ntotal != len(chunks):
        embedder.generate_embeddings(chunks)
        embedder.save_index(INDEX_PATH)

    return embedder, chunks

# -----------------------------
# Main App
# -----------------------------
if uploaded_file:
    embedder, chunks = load_data(uploaded_file)
    generator = Generator()

    st.sidebar.success("✅ Document Loaded")
    st.sidebar.markdown(f"**Total Chunks:** `{len(chunks)}`")

    query = st.text_input("💬 Ask a question about the document:")
    if st.button("🔍 Search") and query.strip():
        if len(chunks) == 0:
            st.error("❌ No chunks found in memory.")
        elif embedder.index is None or embedder.index.ntotal == 0:
            st.error("❌ FAISS index is empty.")
        else:
            with st.spinner("Retrieving relevant context..."):
                results = embedder.search(query, k=5)
            with st.spinner("Generating answer..."):
                answer = generator.generate(query, results)

            st.subheader("📄 Answer")
            st.success(answer)

            with st.expander("🔍 Retrieved Context"):
                for i, chunk in enumerate(results, 1):
                    st.markdown(f"**Chunk {i}:** {chunk}")

    elif query == "":
        st.warning("⚠️ Please enter a question.")
else:
    st.info("📄 Please upload a PDF or TXT file to start.")
