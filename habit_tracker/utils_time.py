from __future__ import annotations

from datetime import date, datetime
from typing import Iterable, Set, Tuple


def parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts)


def normalize_daily(completions: Iterable[str]) -> Set[date]:

    return {parse_iso(ts).date() for ts in completions}


def normalize_weekly(completions: Iterable[str]) -> Set[Tuple[int, int]]:

    out: Set[Tuple[int, int]] = set()
    for ts in completions:
        d = parse_iso(ts).date()
        iso_year, iso_week, _ = d.isocalendar()
        out.add((iso_year, iso_week))
    return out
