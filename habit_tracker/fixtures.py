from __future__ import annotations

from datetime import datetime, timedelta
from typing import List

from habit_tracker.models import Habit


def build_predefined_habits_with_4_weeks_data() -> List[Habit]:
    """
    Returns 5 predefined habits (at least one weekly and one daily)
    with example completion data covering 4 weeks (28 days).
    """

    # 4 daily habits
    workout = Habit(name="Workout", periodicity="daily", description="Gym or home workout")
    reading = Habit(name="Read a book", periodicity="daily", description="Read at least 10 pages")
    walk = Habit(name="Morning walk", periodicity="daily", description="Walk outside for 15-30 minutes")
    teeth = Habit(name="Brush teeth", periodicity="daily", description="Brush teeth (morning/evening)")

    # 1 weekly habit
    drawing = Habit(name="Practice drawing", periodicity="weekly", description="Drawing session once per week")

    # Base date for 4 weeks (28 days)
    start = datetime(2026, 1, 1, 9, 0, 0)

    # --- Daily habits: realistic patterns with some misses ---

    # Workout: miss every 7th day (to show breaks)
    for i in range(28):
        day = start + timedelta(days=i)
        if i % 7 != 0:
            workout.completions.append(day.isoformat())

    # Reading: strong streak, miss only 2 days
    for i in range(28):
        day = start + timedelta(days=i)
        if i not in {10, 23}:
            reading.completions.append(day.replace(hour=20).isoformat())

    # Morning walk: every second day (inconsistent)
    for i in range(28):
        day = start + timedelta(days=i)
        if i % 2 == 0:
            walk.completions.append(day.replace(hour=8).isoformat())

    # Brush teeth: almost perfect, miss 1 day
    for i in range(28):
        day = start + timedelta(days=i)
        if i != 5:
            teeth.completions.append(day.replace(hour=7).isoformat())

    # --- Weekly habit: 4 weeks, skip one week to show a break ---
    # Use Mondays to make ISO-week behavior obvious:
    # 2026-01-05, 2026-01-12, (skip 2026-01-19), 2026-01-26
    weekly_dates = [
        datetime(2026, 1, 5, 18, 0, 0),
        datetime(2026, 1, 12, 18, 0, 0),
        # skip week of Jan 19
        datetime(2026, 1, 26, 18, 0, 0),
    ]
    for d in weekly_dates:
        drawing.completions.append(d.isoformat())

    return [workout, reading, walk, teeth, drawing]
