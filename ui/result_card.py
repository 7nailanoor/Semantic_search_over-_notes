

"""
Search Result Card

Displays semantic search results professionally.

"""

from __future__ import annotations

import streamlit as st

from utils.helpers import truncate_text


class ResultCard:
    """
    UI component for displaying search results.
    """

    @staticmethod
    def show(
        result: dict,
        number: int = 1,
    ):
        """
        Display one search result.

        Parameters
        ----------
        result : dict
            Search result metadata.

        number : int
            Result ranking number.
        """

        filename = result.get("filename", "Unknown Document")

        filetype = result.get("filetype", "")

        page = result.get("page", 1)

        text = result.get("text", "")

        similarity = result.get("similarity", 0)

        final_score = result.get("final_score", similarity)

        with st.container(border=True):
            # Header

            col1, col2 = st.columns([5, 1])

            with col1:
                st.markdown(
                    f"""
                    ### 🔎 Result #{number}

                    **📄 {filename}**

                    Type: `{filetype.upper()}`  
                    Page: `{page}`
                    """
                )

            with col2:
                st.metric("Score", f"{final_score:.2f}")

            st.divider()

            # Content preview

            st.markdown("**Matched Content**")

            st.write(truncate_text(text, 350))

            st.divider()

            # Detailed scores

            col1, col2, col3 = st.columns(3)

            with col1:
                st.caption(f"🧠 Semantic: {similarity:.4f}")

            with col2:
                keyword = result.get("keyword_score", 0)

                st.caption(f"🔤 Keyword: {keyword:.4f}")

            with col3:
                length = result.get("length_score", 0)

                st.caption(f"📏 Context: {length:.4f}")
