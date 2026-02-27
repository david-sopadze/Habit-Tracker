from __future__ import annotations

from datetime import date
from typing import Iterable, List, Optional, Tuple

from habit_tracker.models import Habit
from habit_tracker.utils_time import normalize_daily, normalize_weekly


def list_all_habits(habits: List[Habit]) -> List[Habit]:
    return list(habits)


def habits_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    p = periodicity.strip().lower()
    return [h for h in habits if h.periodicity == p]


def _longest_consecutive_dates(dates: Iterable[date]) -> int:
    s = sorted(set(dates))
    if not s:
        return 0

    best = 1
    current = 1
    for i in range(1, len(s)):
        if (s[i] - s[i - 1]).days == 1:
            current += 1
            best = max(best, current)
        else:
            current = 1
    return best


def _longest_consecutive_iso_weeks(weeks: Iterable[Tuple[int, int]]) -> int:
    wset = set(weeks)
    if not wset:
        return 0

    def next_week(y: int, w: int) -> Tuple[int, int]:
        from datetime import datetime, timedelta

        monday = datetime.fromisocalendar(y, w, 1).date()
        nxt = monday + timedelta(days=7)
        ny, nw, _ = nxt.isocalendar()
        return ny, nw

    best = 0
    for (y, w) in wset:
        from datetime import datetime, timedelta

        monday = datetime.fromisocalendar(y, w, 1).date()
        prev = monday - timedelta(days=7)
        py, pw, _ = prev.isocalendar()

        if (py, pw) in wset:
            continue

        length = 1
        cy, cw = y, w
        while True:
            ny, nw = next_week(cy, cw)
            if (ny, nw) in wset:
                length += 1
                cy, cw = ny, nw
            else:
                break
        best = max(best, length)

    return best


def longest_streak_for_habit(habit: Habit) -> int:
    if habit.periodicity == "daily":
        return _longest_consecutive_dates(normalize_daily(habit.completions))
    if habit.periodicity == "weekly":
        return _longest_consecutive_iso_weeks(normalize_weekly(habit.completions))
    return 0


def longest_streak_overall(habits: List[Habit]) -> int:
    if not habits:
        return 0
    return max(longest_streak_for_habit(h) for h in habits)


def longest_streak_overall_with_habit(habits: List[Habit]) -> Optional[Tuple[str, int]]:

    if not habits:
        return None

    best_habit: Optional[Habit] = None
    best_streak = 0

    for h in habits:
        streak = longest_streak_for_habit(h)
        if streak > best_streak:
            best_streak = streak
            best_habit = h

    if best_habit is None:
        return None

    return best_habit.name, best_streak
