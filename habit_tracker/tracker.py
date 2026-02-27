from __future__ import annotations

from typing import List, Optional, Tuple

from habit_tracker.models import Habit, Task
from habit_tracker.storage_json import JsonStorage


class HabitTracker:
    """
    Controller/service layer:
    - manages habits + tasks in memory
    - persists both via JsonStorage
    """

    def __init__(self, storage: JsonStorage) -> None:
        self.storage = storage
        self._habits: List[Habit] = []
        self._tasks: List[Task] = []

    # --- Persistence ---
    def load(self) -> None:
        habits, tasks = self.storage.load()
        self._habits = habits
        self._tasks = tasks

    def save(self) -> None:
        self.storage.save(self._habits, self._tasks)

    # --- Habits ---
    def replace_all_habits(self, habits: List[Habit]) -> None:
        self._habits = list(habits)
        self.save()

    def create_habit(self, name: str, periodicity: str, description: str = "") -> Habit:
        periodicity = periodicity.strip().lower()
        if periodicity not in {"daily", "weekly"}:
            raise ValueError("Periodicity must be 'daily' or 'weekly'.")

        if self.get_habit_by_name(name) is not None:
            raise ValueError("A habit with this name already exists.")

        habit = Habit(name=name.strip(), periodicity=periodicity, description=description.strip())
        self._habits.append(habit)
        self.save()
        return habit

    def list_habits(self) -> List[Habit]:
        return list(self._habits)

    def list_habits_by_periodicity(self, periodicity: str) -> List[Habit]:
        p = periodicity.strip().lower()
        return [h for h in self._habits if h.periodicity == p]

    def get_habit_by_name(self, name: str) -> Optional[Habit]:
        n = name.strip().lower()
        for h in self._habits:
            if h.name.strip().lower() == n:
                return h
        return None

    def check_off(self, name: str) -> None:
        habit = self.get_habit_by_name(name)
        if habit is None:
            raise ValueError("Habit not found.")
        habit.add_completion()
        self.save()

    def delete_habit(self, name: str) -> None:
        habit = self.get_habit_by_name(name)
        if habit is None:
            raise ValueError("Habit not found.")
        self._habits.remove(habit)
        self.save()

    # --- Tasks (Eisenhower Matrix) ---
    def create_task(
        self,
        title: str,
        urgent: bool,
        important: bool,
        description: str = "",
        due_datetime: Optional[str] = None,
    ) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")

        task = Task(
            title=title,
            urgent=urgent,
            important=important,
            description=description.strip(),
            due_datetime=due_datetime.strip() if due_datetime else None,
        )
        self._tasks.append(task)
        self.save()
        return task

    def list_tasks(self) -> List[Task]:
        return list(self._tasks)

    def list_tasks_by_quadrant(self, quadrant: int) -> List[Task]:
        """
        Quadrants:
        1 = urgent+important
        2 = important only
        3 = urgent only
        4 = neither
        """
        if quadrant not in {1, 2, 3, 4}:
            raise ValueError("Quadrant must be 1, 2, 3, or 4.")

        def in_quad(t: Task) -> bool:
            if quadrant == 1:
                return t.urgent and t.important
            if quadrant == 2:
                return (not t.urgent) and t.important
            if quadrant == 3:
                return t.urgent and (not t.important)
            return (not t.urgent) and (not t.important)

        return [t for t in self._tasks if in_quad(t)]

    def mark_task_completed(self, index: int) -> None:
        tasks = self.list_tasks()
        if index < 1 or index > len(tasks):
            raise ValueError("Invalid task number.")
        tasks[index - 1].completed = True
        self._tasks = tasks
        self.save()

    def delete_task(self, index: int) -> None:
        tasks = self.list_tasks()
        if index < 1 or index > len(tasks):
            raise ValueError("Invalid task number.")
        del tasks[index - 1]
        self._tasks = tasks
        self.save()
