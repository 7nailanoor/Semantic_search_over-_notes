

"""
Advanced Result Ranking Module

Ranks semantic search results using:

- Semantic similarity
- Keyword matching
- Exact phrase matching
- Section heading importance
- Context quality

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
