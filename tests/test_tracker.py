import pytest
from pathlib import Path

from habit_tracker.storage_json import JsonStorage
from habit_tracker.tracker import HabitTracker


def make_tracker(tmp_path: Path) -> HabitTracker:
    storage = JsonStorage(file_path=str(tmp_path / "data.json"))
    tracker = HabitTracker(storage=storage)
    tracker.load()
    return tracker


def test_create_habit_and_list(tmp_path: Path):
    t = make_tracker(tmp_path)
    t.create_habit("Workout", "daily", "Exercise 20 minutes")
    assert len(t.list_habits()) == 1
    assert t.list_habits()[0].name == "Workout"


def test_check_off_adds_completion(tmp_path: Path):
    t = make_tracker(tmp_path)
    t.create_habit("Read", "daily")
    t.check_off("Read")
    habit = t.get_habit_by_name("Read")
    assert habit is not None
    assert len(habit.completions) == 1


def test_rejects_invalid_periodicity(tmp_path: Path):
    t = make_tracker(tmp_path)
    with pytest.raises(ValueError):
        t.create_habit("Bad", "monthly")
