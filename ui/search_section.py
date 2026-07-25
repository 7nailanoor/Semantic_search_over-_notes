"""
Search Section

Displays the semantic search interface.

Author: Naila Noor
Project: Semantic Search over Notes
"""

from __future__ import annotations

import streamlit as st

from utils.constants import DEFAULT_TOP_K


class SearchSection:
    """
    Search interface.
    """

    @staticmethod
    def show():
        """
        Display search controls.

        Returns
        -------
        tuple[str, int, bool]
            query, top_k, search_button
        """

        st.subheader("🔍 Semantic Search")

        st.caption(
            "Ask questions naturally. AI will search across your indexed documents."
        )

        query = st.text_input(
            "Ask a question",
            placeholder="Example: What tools and technologies are used in this project?",
        )

        col1, col2 = st.columns([1, 4])

        with col1:
            top_k = st.selectbox(
                "Results",
                options=[1, 3, 5, 10],
                index=2,
            )

        with col2:
            st.write("")
            st.write("")

            search_clicked = st.button(
                "🔎 Search",
                use_container_width=True,
                type="primary",
            )

        return query.strip(), top_k, search_clicked
