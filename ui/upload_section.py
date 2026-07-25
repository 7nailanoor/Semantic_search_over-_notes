"""
Upload Section

Professional upload interface for Semantic Search.

"""

from __future__ import annotations

from pathlib import Path
from typing import List

import streamlit as st

from utils.helpers import format_file_size


class UploadSection:
    """
    Handles document upload UI.
    """

    FILE_ICONS = {
        ".pdf": "📕",
        ".docx": "📘",
        ".txt": "📄",
    }

    @classmethod
    def show(cls) -> List:
        """
        Display upload interface.

        Returns
        -------
        list
            Uploaded Streamlit files.
        """

        st.subheader("📂 Upload Documents")

        st.caption(
            "Upload PDF, DOCX or TXT documents to create an AI-powered semantic search index."
        )

        uploaded_files = st.file_uploader(
            label="Choose documents",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            help="Supported formats: PDF, DOCX and TXT",
            label_visibility="collapsed",
            key="document_uploader",
        )

        if not uploaded_files:
            st.info("Drag and drop files above or click Browse files.")

            return []

        st.success(f"✅ {len(uploaded_files)} document(s) selected")

        total_size = sum(file.size for file in uploaded_files)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("📄 Documents", len(uploaded_files))

        with col2:
            st.metric("💾 Total Size", format_file_size(total_size))

        st.divider()

        st.markdown("### 📑 Selected Files")

        with st.container(border=True):
            for file in uploaded_files:
                extension = Path(file.name).suffix.lower()

                icon = cls.FILE_ICONS.get(extension, "📄")

                col1, col2 = st.columns([5, 1])

                with col1:
                    st.write(f"{icon} **{file.name}**")

                with col2:
                    st.caption(format_file_size(file.size))

        st.divider()

        st.info(
            "Ready for indexing. Click **Build Search Index** below to process documents."
        )

        return uploaded_files
