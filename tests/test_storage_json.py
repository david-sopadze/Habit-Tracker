import json
from pathlib import Path

from habit_tracker.storage_json import JsonStorage
from habit_tracker.models import Habit


def test_save_and_load_habits_roundtrip(tmp_path: Path):
    file_path = tmp_path / "data.json"
    storage = JsonStorage(file_path=str(file_path))

    habits = [Habit(name="Workout", periodicity="daily")]
    storage.save_habits(habits)

    loaded = storage.load_habits()
    assert len(loaded) == 1
    assert loaded[0].name == "Workout"
    assert loaded[0].periodicity == "daily"

    # also ensure JSON has expected top-level key
    raw = json.loads(file_path.read_text(encoding="utf-8"))
    assert "habits" in raw
