"""
Sidebar

Displays application information and statistics.

Author: Naila Noor
Project: Semantic Search over Notes
"""

from __future__ import annotations

import streamlit as st


class Sidebar:
    """
    Sidebar UI.
    """

    @staticmethod
    def show(
        total_documents: int = 0,
        total_chunks: int = 0,
        total_vectors: int = 0,
    ):
        """
        Render sidebar.
        """

        with st.sidebar:
            st.image(
                "assets/logo.png",
                use_container_width=True,
            )

            st.title("Semantic Search")

            st.caption("Search PDFs, DOCX and TXT files using AI embeddings.")

            st.divider()

            st.subheader("📈 Index Statistics")

            st.metric(
                "Documents",
                total_documents,
            )

            st.metric(
                "Chunks",
                total_chunks,
            )

            st.metric(
                "Vectors",
                total_vectors,
            )

            st.divider()

            st.subheader("📚 Supported Files")

            st.success("PDF")

            st.success("DOCX")

            st.success("TXT")

            st.divider()

            st.subheader("💡 Tips")

            st.markdown(
                """
- Ask complete questions.
- Use descriptive keywords.
- Upload multiple documents.
- Results are ranked by semantic similarity.
                """
            )

            st.divider()

            st.caption("Made with ❤️ using Streamlit + FAISS")
