"""
Semantic Search over Notes

AI-powered semantic search across PDF, DOCX and TXT documents.

Author: Naila Noor
Project: Semantic Search over Notes
"""

from __future__ import annotations

from pathlib import Path
import time

import streamlit as st


from documents.loader import DocumentLoader

from preprocessing.cleaner import TextCleaner
from preprocessing.chunker import TextChunker

from embeddings.generate_embeddings import EmbeddingGenerator

from vector_store.faiss_manager import FAISSManager

from search.semantic_search import SemanticSearch


from ui.sidebar import Sidebar
from ui.upload_section import UploadSection
from ui.search_section import SearchSection
from ui.dashboard import Dashboard
from ui.result_card import ResultCard


from utils.file_handler import FileHandler

from settings import Settings


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Semantic Search over Notes",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# INITIALIZE SETTINGS
# ==========================================================

Settings.initialize()


# ==========================================================
# LOAD CSS
# ==========================================================


def load_css():

    css_file = Settings.ASSETS_DIR / "styles.css"

    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as file:
            st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


load_css()


# ==========================================================
# SESSION STATE
# ==========================================================

SESSION_DEFAULTS = {
    "documents": 0,
    "chunks": 0,
    "indexed": False,
    "processing_time": 0,
    "search_time": 0,
    "results": [],
    "last_query": "",
}


for key, value in SESSION_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# INITIALIZE COMPONENTS
# ==========================================================

file_handler = FileHandler()

chunker = TextChunker()

embedding_generator = EmbeddingGenerator()

faiss_manager = FAISSManager()


semantic_search = SemanticSearch()

# Important:
# Use the same FAISS index for indexing and searching

semantic_search.faiss = faiss_manager


# ==========================================================
# HEADER
# ==========================================================


def page_header():

    # st.markdown(
    #     """
    #     <div class="main-title">
    #     📚 Semantic Search over Notes
    #     </div>
    #     """,
    #     unsafe_allow_html=True,
    # )
    st.markdown(
        """
        <h1 style="font-size:28px; margin-bottom:0;">
            📚 Semantic Search over Notes
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sub-title">
        Search your documents using AI embeddings and FAISS vector search.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# RESET SEARCH
# ==========================================================


def reset_search():

    st.session_state.results = []

    st.session_state.last_query = ""

    st.session_state.search_time = 0


# ==========================================================
# BUILD INDEX
# ==========================================================


def build_index(uploaded_files):

    if not uploaded_files:
        return

    # Remove old vectors

    faiss_manager.clear()

    progress = st.progress(0)

    status = st.empty()

    total_chunks = 0

    start = time.perf_counter()

    for index, uploaded_file in enumerate(uploaded_files):
        status.info(f"Processing {uploaded_file.name}")

        # -------------------------------
        # Save File
        # -------------------------------

        file_path = file_handler.save_uploaded_file(uploaded_file)

        # -------------------------------
        # Load Document
        # -------------------------------

        loader = DocumentLoader(file_path)

        document = loader.load()

        # -------------------------------
        # Clean Document
        # -------------------------------

        document = TextCleaner.clean_document(document)

        # -------------------------------
        # Chunk Document
        # -------------------------------

        chunks = chunker.chunk_document(document)

        total_chunks += len(chunks)

        # -------------------------------
        # Generate Embeddings
        # -------------------------------

        embedded_chunks = embedding_generator.generate(chunks)

        # -------------------------------
        # Add to FAISS
        # -------------------------------

        faiss_manager.add_documents(embedded_chunks)

        progress.progress((index + 1) / len(uploaded_files))

    # Save index

    faiss_manager.save()

    elapsed = time.perf_counter() - start

    st.session_state.documents = len(uploaded_files)

    st.session_state.chunks = total_chunks

    st.session_state.processing_time = elapsed

    st.session_state.indexed = True

    reset_search()

    status.success("✅ Semantic index created successfully")


# ==========================================================
# SIDEBAR
# ==========================================================


def render_sidebar():

    Sidebar.show(
        total_documents=st.session_state.documents,
        total_chunks=st.session_state.chunks,
        total_vectors=faiss_manager.total_vectors,
    )


# ==========================================================
# DASHBOARD
# ==========================================================


def render_dashboard():

    Dashboard.show(
        documents=st.session_state.documents,
        chunks=st.session_state.chunks,
        vectors=faiss_manager.total_vectors,
        processing_time=st.session_state.processing_time,
    )


# ==========================================================
# UPLOAD SECTION
# ==========================================================


def render_upload():

    uploaded_files = UploadSection.show()

    if uploaded_files:
        if st.button(
            "🚀 Build Search Index",
            use_container_width=True,
            type="primary",
            key="build_search_index_button",
        ):
            try:
                with st.spinner("Creating AI search index..."):
                    build_index(uploaded_files)

            except Exception as error:
                st.error(f"Indexing failed:\n{error}")


# ==========================================================
# SEARCH
# ==========================================================


def render_search():

    query, top_k, clicked = SearchSection.show()

    if clicked:
        if not query:
            st.warning("Please enter a question.")

            return

        if not st.session_state.indexed:
            st.warning("Please upload documents first.")

            return

        start = time.perf_counter()

        with st.spinner("Searching..."):
            results = semantic_search.search(query=query, top_k=top_k)

        elapsed = time.perf_counter() - start

        st.session_state.results = results

        st.session_state.last_query = query

        st.session_state.search_time = elapsed

    show_results()


# ==========================================================
# RESULTS
# ==========================================================


def show_results():

    if not st.session_state.results:
        return

    st.subheader("📌 Search Results")

    st.caption(
        f"""
Query:
{st.session_state.last_query}

Search time:
{st.session_state.search_time:.3f}s
"""
    )

    for number, result in enumerate(st.session_state.results, start=1):
        ResultCard.show(result=result, number=number)


# ==========================================================
# FOOTER
# ==========================================================


def footer():

    st.divider()

    st.markdown(
        """
        <center>
        Built with ❤️ using Python,
        Streamlit, Sentence Transformers and FAISS
        </center>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# MAIN
# ==========================================================


def main():

    render_sidebar()

    page_header()

    st.divider()

    render_dashboard()

    st.divider()

    render_upload()

    st.divider()

    render_search()

    footer()


if __name__ == "__main__":
    main()
