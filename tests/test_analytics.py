from datetime import datetime, timedelta

from habit_tracker.models import Habit
from habit_tracker.analytics import (
    longest_streak_for_habit,
    longest_streak_overall,
    longest_streak_overall_with_habit,
    habits_by_periodicity,
)


def test_daily_longest_streak_simple():
    h = Habit(name="Workout", periodicity="daily")
    base = datetime(2026, 1, 1, 10, 0, 0)
    for i in range(5):
        h.completions.append((base + timedelta(days=i)).isoformat())

    assert longest_streak_for_habit(h) == 5


def test_daily_duplicates_same_day_count_once():
    h = Habit(name="Read", periodicity="daily")
    day = datetime(2026, 1, 2, 9, 0, 0)
    h.completions.append(day.isoformat())
    h.completions.append(day.replace(hour=21).isoformat())

    assert longest_streak_for_habit(h) == 1


def test_weekly_longest_streak_simple():
    h = Habit(name="Drawing", periodicity="weekly")
    h.completions.append(datetime(2026, 1, 5, 10, 0).isoformat())
    h.completions.append(datetime(2026, 1, 12, 10, 0).isoformat())
    h.completions.append(datetime(2026, 1, 19, 10, 0).isoformat())

    assert longest_streak_for_habit(h) == 3


def test_longest_streak_overall():
    a = Habit(name="A", periodicity="daily")
    b = Habit(name="B", periodicity="daily")

    base = datetime(2026, 1, 1, 10, 0, 0)
    for i in range(2):
        a.completions.append((base + timedelta(days=i)).isoformat())
    for i in range(4):
        b.completions.append((base + timedelta(days=i)).isoformat())

    assert longest_streak_overall([a, b]) == 4


def test_longest_streak_overall_with_habit():
    a = Habit(name="A", periodicity="daily")
    b = Habit(name="B", periodicity="daily")

    base = datetime(2026, 1, 1, 10, 0, 0)
    for i in range(2):
        a.completions.append((base + timedelta(days=i)).isoformat())
    for i in range(4):
        b.completions.append((base + timedelta(days=i)).isoformat())

    name, streak = longest_streak_overall_with_habit([a, b])
    assert name == "B"
    assert streak == 4


def test_filter_by_periodicity():
    habits = [
        Habit(name="W", periodicity="weekly"),
        Habit(name="D1", periodicity="daily"),
        Habit(name="D2", periodicity="daily"),
    ]
    daily = habits_by_periodicity(habits, "daily")
    assert [h.name for h in daily] == ["D1", "D2"]
