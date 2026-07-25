"""
Timer Utility

Measures execution time for indexing,
embedding generation, and semantic search.

Author: Naila Noor
Project: Semantic Search over Notes
"""

from __future__ import annotations

import time


class Timer:
    """
    Simple timer utility.
    """

    def __init__(self):

        self.start_time = None
        self.end_time = None

    # ---------------------------------------------------------

    def start(self):
        """
        Start the timer.
        """

        self.start_time = time.perf_counter()

    # ---------------------------------------------------------

    def stop(self) -> float:
        """
        Stop the timer.

        Returns
        -------
        float
            Elapsed time in seconds.
        """

        if self.start_time is None:
            raise RuntimeError("Timer has not been started.")

        self.end_time = time.perf_counter()

        return self.elapsed_time()

    # ---------------------------------------------------------

    def elapsed_time(self) -> float:
        """
        Return elapsed time in seconds.
        """

        if self.start_time is None:
            raise RuntimeError("Timer has not been started.")

        end = self.end_time if self.end_time is not None else time.perf_counter()

        return round(end - self.start_time, 4)

    # ---------------------------------------------------------

    def reset(self):
        """
        Reset the timer.
        """

        self.start_time = None
        self.end_time = None

    # ---------------------------------------------------------

    def elapsed_ms(self) -> float:
        """
        Return elapsed time in milliseconds.
        """

        return round(self.elapsed_time() * 1000, 2)

    # ---------------------------------------------------------

    def __enter__(self):
        """
        Context manager support.
        """

        self.start()

        return self

    # ---------------------------------------------------------

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):
        """
        Stop timer automatically.
        """

        self.stop()
