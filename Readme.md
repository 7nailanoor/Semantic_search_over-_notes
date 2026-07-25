# 📚 Semantic Search over Notes

An AI-powered semantic search application that allows users to search across **PDF, DOCX, and TXT documents** using natural language. Instead of relying on exact keyword matching, the system understands the semantic meaning of queries using transformer-based embeddings and retrieves the most relevant document sections.

---

## 🚀 Features

* 📄 Upload multiple PDF, DOCX, and TXT documents
* 🧹 Automatic text cleaning and preprocessing
* ✂️ Intelligent text chunking with overlap
* 🧠 Generate semantic embeddings using Sentence Transformers
* ⚡ Fast vector similarity search using FAISS
* 🔍 Natural language search
* 📊 Interactive Streamlit dashboard
* 📑 Displays document name, page number, similarity score, and matched content
* 🎨 Clean and responsive user interface

---

## 🛠️ Tech Stack

### Programming Language

* Python

### Frontend

* Streamlit

### AI & NLP

* Sentence Transformers
* NumPy

### Vector Database

* FAISS

### Document Processing

* PyMuPDF (PDF)
* python-docx (DOCX)

### Utilities

* pathlib
* logging
* typing
* regex

---

## 📂 Project Structure

```text
semantic_search/
│
├── app.py
├── settings.py
│
├── assets/
│   └── styles.css
│
├── data/
│   ├── uploaded_files/
│   └── extracted_text/
│
├── documents/
│   ├── loader.py
│   ├── base_reader.py
│   ├── pdf_reader.py
│   ├── docx_reader.py
│   └── txt_reader.py
│
├── preprocessing/
│   ├── cleaner.py
│   └── chunker.py
│
├── embeddings/
│   ├── embedding_model.py
│   └── generate_embeddings.py
│
├── vector_store/
│   ├── faiss_manager.py
│   └── metadata_store.py
│
├── search/
│   ├── semantic_search.py
│   ├── ranking.py
│   └── similarity.py
│
├── ui/
│   ├── sidebar.py
│   ├── dashboard.py
│   ├── upload_section.py
│   ├── search_section.py
│   └── result_card.py
│
└── utils/
    ├── helpers.py
    ├── constants.py
    └── file_handler.py
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/semantic-search-over-notes.git
cd semantic-search-over-notes
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will automatically open in your browser.

---

## 🔍 How It Works

1. Upload one or more PDF, DOCX, or TXT files.
2. The application extracts text from each document.
3. The text is cleaned and divided into meaningful chunks.
4. Each chunk is converted into a semantic embedding.
5. Embeddings are indexed using FAISS.
6. User queries are converted into embeddings.
7. FAISS retrieves the most similar chunks.
8. A hybrid ranking system orders the results.
9. The best matching document sections are displayed.

---

## 🧠 Search Pipeline

```text
Upload Documents
        │
        ▼
Document Loader
        │
        ▼
Text Cleaning
        │
        ▼
Text Chunking
        │
        ▼
Embedding Generation
        │
        ▼
FAISS Indexing
        │
        ▼
Semantic Search
        │
        ▼
Hybrid Ranking
        │
        ▼
Relevant Results
```

---

## 📸 Screenshots

Add screenshots of:

* Home Page
* Document Upload
* Dashboard
* Search Results
* Indexed Documents

---

## 📈 Future Improvements

* Section-aware intelligent chunking
* Stronger embedding models (BGE/E5)
* Hybrid semantic + keyword retrieval
* Metadata-aware ranking
* Highlight matched text
* Search history
* Search analytics dashboard
* Multi-language document support
* OCR support for scanned PDFs
* RAG integration with Large Language Models
* Answer generation using local or cloud LLMs

---

## 🎯 Learning Outcomes

This project demonstrates practical knowledge of:

* Natural Language Processing (NLP)
* Semantic Search
* Transformer Embeddings
* Vector Databases
* FAISS Indexing
* Information Retrieval
* Streamlit Application Development
* Modular Python Project Design

---
