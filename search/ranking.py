# """
# Ranking Module

# Hybrid ranking system for semantic search.

# Ranking signals:
# - Semantic similarity from FAISS
# - Keyword relevance
# - Query intent matching
# - Context quality

# Author: Naila Noor
# Project: Semantic Search over Notes
# """

# from __future__ import annotations

# import re
# from typing import List, Dict, Any


# class ResultRanker:
#     """
#     Improves FAISS results using multiple ranking signals.
#     """

#     def __init__(
#         self,
#         semantic_weight: float = 0.60,
#         keyword_weight: float = 0.25,
#         context_weight: float = 0.10,
#         length_weight: float = 0.05,
#     ):

#         self.semantic_weight = semantic_weight
#         self.keyword_weight = keyword_weight
#         self.context_weight = context_weight
#         self.length_weight = length_weight

#     # -----------------------------------------------------
#     # Keyword Extraction
#     # -----------------------------------------------------

#     @staticmethod
#     def _extract_keywords(text: str) -> set:
#         """
#         Extract meaningful words.
#         """

#         words = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())

#         stop_words = {"what", "which", "how", "is", "are", "the", "a", "an", "used"}

#         return {word for word in words if word not in stop_words}

#     # -----------------------------------------------------
#     # Keyword Matching
#     # -----------------------------------------------------

#     def _keyword_score(
#         self,
#         query: str,
#         text: str,
#     ) -> float:
#         """
#         Measures keyword overlap.
#         """

#         query_words = self._extract_keywords(query)

#         text_words = self._extract_keywords(text)

#         if not query_words:
#             return 0.0

#         matched = query_words.intersection(text_words)

#         return len(matched) / len(query_words)

#     # -----------------------------------------------------
#     # Query Intent Detection
#     # -----------------------------------------------------

#     def _context_score(
#         self,
#         query: str,
#         text: str,
#     ) -> float:
#         """
#         Detect whether a chunk contains
#         answer-like context.

#         Works for many document types.
#         """

#         query = query.lower()
#         text = text.lower()

#         score = 0

#         context_patterns = [
#             # Technology questions
#             (
#                 [
#                     "tool",
#                     "technology",
#                     "stack",
#                     "framework",
#                     "library",
#                     "software",
#                     "built",
#                     "developed",
#                     "using",
#                 ],
#                 [
#                     "python",
#                     "java",
#                     "javascript",
#                     "flask",
#                     "django",
#                     "mysql",
#                     "react",
#                     "html",
#                     "css",
#                     "bootstrap",
#                     "api",
#                 ],
#             ),
#             # Feature questions
#             (
#                 [
#                     "feature",
#                     "function",
#                     "capability",
#                 ],
#                 [
#                     "allows",
#                     "provides",
#                     "supports",
#                     "includes",
#                 ],
#             ),
#             # Challenge questions
#             (
#                 [
#                     "challenge",
#                     "problem",
#                     "issue",
#                 ],
#                 [
#                     "error",
#                     "difficulty",
#                     "solved",
#                     "fixed",
#                 ],
#             ),
#         ]

#         for query_terms, answer_terms in context_patterns:
#             if any(term in query for term in query_terms):
#                 if any(term in text for term in answer_terms):
#                     score += 1

#         return min(score, 1.0)

#     # -----------------------------------------------------
#     # Chunk Quality
#     # -----------------------------------------------------

#     @staticmethod
#     def _length_score(text: str) -> float:
#         """
#         Avoid extremely small chunks.
#         """

#         words = len(text.split())

#         if words < 30:
#             return 0.3

#         if words < 120:
#             return 1.0

#         if words <= 250:
#             return 0.8

#         return 0.5

#     # -----------------------------------------------------
#     # Ranking
#     # -----------------------------------------------------

#     def rank(
#         self,
#         query: str,
#         results: List[Dict[str, Any]],
#     ) -> List[Dict[str, Any]]:
#         """
#         Rank retrieved chunks.
#         """

#         ranked_results = []

#         for result in results:
#             text = result.get("text", "")

#             semantic = result.get("similarity", 0)

#             keyword = self._keyword_score(query, text)

#             context = self._context_score(query, text)

#             length = self._length_score(text)

#             final_score = (
#                 semantic * self.semantic_weight
#                 + keyword * self.keyword_weight
#                 + context * self.context_weight
#                 + length * self.length_weight
#             )

#             result["semantic_score"] = round(semantic, 4)

#             result["keyword_score"] = round(keyword, 4)

#             result["context_score"] = round(context, 4)

#             result["length_score"] = round(length, 4)

#             result["final_score"] = round(final_score, 4)

#             ranked_results.append(result)

#         ranked_results.sort(key=lambda x: x["final_score"], reverse=True)

#         return ranked_results


"""
Advanced Result Ranking Module

Ranks semantic search results using:

- Semantic similarity
- Keyword matching
- Exact phrase matching
- Section heading importance
- Context quality

Author: Naila Noor
Project: Semantic Search over Notes
"""

from __future__ import annotations

import re
from typing import List, Dict, Any


class ResultRanker:
    """
    Hybrid ranking system for semantic search.
    """

    def __init__(self):

        # Weight distribution

        self.semantic_weight = 0.55

        self.keyword_weight = 0.20

        self.exact_weight = 0.20

        self.context_weight = 0.05

    # =====================================================
    # Extract words
    # =====================================================

    @staticmethod
    def _extract_keywords(text: str) -> set:
        """
        Extract useful words.
        """

        words = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())

        stop_words = {"what", "is", "are", "the", "of", "a", "an", "this", "in", "used"}

        return {word for word in words if word not in stop_words}

    # =====================================================
    # Keyword Score
    # =====================================================

    def _keyword_score(self, query: str, text: str) -> float:
        """
        Measures keyword overlap.
        """

        query_words = self._extract_keywords(query)

        text_words = self._extract_keywords(text)

        if not query_words:
            return 0.0

        matches = query_words.intersection(text_words)

        return len(matches) / len(query_words)

    # =====================================================
    # Exact Match Score
    # =====================================================

    def _exact_match_score(self, query: str, text: str) -> float:
        """
        Gives bonus when important query
        words appear exactly.
        """

        query_words = self._extract_keywords(query)

        text_lower = text.lower()

        if not query_words:
            return 0.0

        matched = 0

        for word in query_words:
            if word in text_lower:
                matched += 1

        return matched / len(query_words)

    # =====================================================
    # Section Importance
    # =====================================================

    def _section_score(self, query: str, result: Dict[str, Any]) -> float:
        """
        Boost matching headings.

        Example:

        Query:
        what is conclusion

        Section:
        7. Conclusion

        gets higher score.
        """

        section = result.get("section", "").lower()

        if not section:
            return 0.0

        query_words = self._extract_keywords(query)

        matches = 0

        for word in query_words:
            if word in section:
                matches += 1

        if not query_words:
            return 0.0

        return matches / len(query_words)

    # =====================================================
    # Rank Results
    # =====================================================

    def rank(self, query: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        ranked_results = []

        for result in results:
            semantic = float(result.get("similarity", 0))

            keyword = self._keyword_score(query, result.get("text", ""))

            exact = self._exact_match_score(query, result.get("text", ""))

            section = self._section_score(query, result)

            final_score = (
                semantic * self.semantic_weight
                + keyword * self.keyword_weight
                + exact * self.exact_weight
                + section * self.context_weight
            )

            result["semantic_score"] = round(semantic, 4)

            result["keyword_score"] = round(keyword, 4)

            result["exact_score"] = round(exact, 4)

            result["section_score"] = round(section, 4)

            result["final_score"] = round(final_score, 4)

            ranked_results.append(result)

        ranked_results.sort(key=lambda x: x["final_score"], reverse=True)

        return ranked_results
