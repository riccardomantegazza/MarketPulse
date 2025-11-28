"""Domain models shared across the project."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class MarketEvent:
    """Time window that represents a relevant market regime."""

    name: str
    start: pd.Timestamp
    end: pd.Timestamp | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "start", pd.Timestamp(self.start))
        if self.end is not None:
            object.__setattr__(self, "end", pd.Timestamp(self.end))

    def contains(self, date: pd.Timestamp) -> bool:
        """Return True if the provided date is inside the event window."""
        ts = pd.Timestamp(date)
        after_start = ts >= self.start
        before_end = True if self.end is None else ts <= self.end
        return after_start and before_end

    def as_slice(self) -> slice:
        """Return a convenient slice usable with pandas indexers."""
        return slice(self.start, self.end)

