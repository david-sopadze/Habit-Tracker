from pathlib import Path

from habit_tracker.storage_json import JsonStorage
from habit_tracker.tracker import HabitTracker


def make_tracker(tmp_path: Path) -> HabitTracker:
    storage = JsonStorage(file_path=str(tmp_path / "data.json"))
    t = HabitTracker(storage=storage)
    t.load()
    return t


def test_create_task_and_persist(tmp_path: Path):
    t = make_tracker(tmp_path)
    t.create_task("Doctor appointment", urgent=True, important=True, due_datetime="12/01/26 14:30")
    t2 = make_tracker(tmp_path)
    assert len(t2.list_tasks()) == 1
    assert t2.list_tasks()[0].title == "Doctor appointment"


def test_task_quadrants(tmp_path: Path):
    t = make_tracker(tmp_path)
    t.create_task("Q1", urgent=True, important=True)
    t.create_task("Q2", urgent=False, important=True)
    t.create_task("Q3", urgent=True, important=False)
    t.create_task("Q4", urgent=False, important=False)

    assert len(t.list_tasks_by_quadrant(1)) == 1
    assert len(t.list_tasks_by_quadrant(2)) == 1
    assert len(t.list_tasks_by_quadrant(3)) == 1
    assert len(t.list_tasks_by_quadrant(4)) == 1
