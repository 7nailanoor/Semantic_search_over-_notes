# """
# Dashboard UI

# Author: Naila Noor
# Project: Semantic Search over Notes
# """

# from __future__ import annotations

# import streamlit as st


# class Dashboard:
#     @staticmethod
#     def show(
#         total_documents: int,
#         total_chunks: int,
#         total_vectors: int,
#     ) -> None:

#         st.subheader("📊 Dashboard")

#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.metric(
#                 label="📄 Documents",
#                 value=total_documents,
#             )

#         with col2:
#             st.metric(
#                 label="🧩 Chunks",
#                 value=total_chunks,
#             )

#         with col3:
#             st.metric(
#                 label="🧠 Vectors",
#                 value=total_vectors,
#             )

#         st.divider()

"""
Dashboard UI Component

Displays project statistics and analytics.

Author: Naila Noor
Project: Semantic Search over Notes
"""

import streamlit as st


class Dashboard:
    """
    Dashboard component for displaying
    semantic search statistics.
    """

    @staticmethod
    def show(
        documents: int = 0,
        chunks: int = 0,
        vectors: int = 0,
        processing_time: float = 0.0,
    ):
        """
        Display dashboard metrics.
        """

        st.subheader("📊 Project Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(label="📄 Documents", value=documents)

        with col2:
            st.metric(label="🧩 Text Chunks", value=chunks)

        with col3:
            st.metric(label="🧠 Vectors", value=vectors)

        with col4:
            st.metric(label="⚡ Processing Time", value=f"{processing_time:.2f}s")

        st.divider()

        st.markdown(
            """
            <div class="dashboard-info">

            <h4>How Semantic Search Works</h4>

            <p>
            Documents are converted into AI embeddings,
            stored inside a FAISS vector database,
            and retrieved using similarity search.
            </p>

            </div>
            """,
            unsafe_allow_html=True,
        )
