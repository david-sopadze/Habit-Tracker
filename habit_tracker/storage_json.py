from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple

from habit_tracker.models import Habit, Task


class JsonStorage:
    def __init__(self, file_path: str = "data.json") -> None:
        self.path = Path(file_path)

    # ----------------------------
    # New API (habits + tasks)
    # ----------------------------
    def load(self) -> Tuple[List[Habit], List[Task]]:
        if not self.path.exists():
            return [], []

        raw = json.loads(self.path.read_text(encoding="utf-8"))

        habits_raw = raw.get("habits", [])
        tasks_raw = raw.get("tasks", [])

        habits = [Habit.from_dict(h) for h in habits_raw]
        tasks = [Task.from_dict(t) for t in tasks_raw]
        return habits, tasks

    def save(self, habits: List[Habit], tasks: List[Task]) -> None:
        payload = {
            "habits": [h.to_dict() for h in habits],
            "tasks": [t.to_dict() for t in tasks],
        }
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    # ----------------------------
    # Backwards-compatible API
    # (to keep older tests working)
    # ----------------------------
    def load_habits(self) -> List[Habit]:
        habits, _tasks = self.load()
        return habits

    def save_habits(self, habits: List[Habit]) -> None:
        # Preserve existing tasks in the file (if any)
        _old_habits, tasks = self.load()
        self.save(habits, tasks)
