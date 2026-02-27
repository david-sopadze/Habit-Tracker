from __future__ import annotations

from habit_tracker.analytics import (
    habits_by_periodicity,
    list_all_habits,
    longest_streak_for_habit,
    longest_streak_overall_with_habit,
)
from habit_tracker.fixtures import build_predefined_habits_with_4_weeks_data
from habit_tracker.storage_json import JsonStorage
from habit_tracker.tracker import HabitTracker



def _ask_int(prompt: str, min_value: int | None = None, max_value: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
        except ValueError:
            print("Please enter a number.")
            continue

        if min_value is not None and val < min_value:
            print(f"Please enter a number >= {min_value}.")
            continue
        if max_value is not None and val > max_value:
            print(f"Please enter a number <= {max_value}.")
            continue
        return val


def _ask_yes_no(prompt: str) -> bool:
    while True:
        raw = input(prompt).strip().lower()
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        print("Please type y/n.")


def _print_habits_numbered(habits) -> None:
    if not habits:
        print("No habits found.")
        return
    for i, h in enumerate(habits, start=1):
        print(f"{i}) {h.name} [{h.periodicity}] (completions: {len(h.completions)})")


def _choose_habit(tracker: HabitTracker) -> str | None:
    habits = tracker.list_habits()
    if not habits:
        print("No habits available.")
        return None

    _print_habits_numbered(habits)
    idx = _ask_int("Choose habit number: ", 1, len(habits))
    return habits[idx - 1].name


def _print_tasks_numbered(tasks) -> None:
    if not tasks:
        print("No tasks found.")
        return
    for i, t in enumerate(tasks, start=1):
        status = "DONE" if t.completed else "TODO"
        quad = (
            "Q1" if (t.urgent and t.important)
            else "Q2" if ((not t.urgent) and t.important)
            else "Q3" if (t.urgent and (not t.important))
            else "Q4"
        )
        due = f" | due: {t.due_datetime}" if t.due_datetime else ""
        print(f"{i}) [{status}] [{quad}] {t.title}{due}")


# ---------- Menus ----------

def _analytics_menu(tracker: HabitTracker) -> None:
    while True:
        print("\n--- Analytics ---")
        print("1) List all habits")
        print("2) List habits by periodicity")
        print("3) Longest streak overall (with habit name)")
        print("4) Longest streak for a habit (pick by number)")
        print("5) Back")

        choice = input("Select an option: ").strip()

        if choice == "1":
            habits = list_all_habits(tracker.list_habits())
            _print_habits_numbered(habits)

        elif choice == "2":
            p = input("Periodicity (daily/weekly): ").strip()
            habits = habits_by_periodicity(tracker.list_habits(), p)
            _print_habits_numbered(habits)

        elif choice == "3":
            result = longest_streak_overall_with_habit(tracker.list_habits())
            if result is None:
                print("No habits available.")
            else:
                name, streak = result
                print(f"Longest streak overall: {streak} (Habit: {name})")

        elif choice == "4":
            name = _choose_habit(tracker)
            if name is None:
                continue
            habit = tracker.get_habit_by_name(name)
            if habit is None:
                print("Habit not found.")
            else:
                value = longest_streak_for_habit(habit)
                print(f"Longest streak for '{habit.name}': {value}")

        elif choice == "5":
            break
        else:
            print("Invalid option. Try again.")


def _task_matrix_menu(tracker: HabitTracker) -> None:
    while True:
        print("\n--- Eisenhower Matrix ---")
        print("1) Add task")
        print("2) List all tasks")
        print("3) List tasks by quadrant (1-4)")
        print("4) Mark task completed (pick by number)")
        print("5) Delete task (pick by number)")
        print("6) Back")

        choice = input("Select an option: ").strip()

        try:
            if choice == "1":
                title = input("Task title: ").strip()
                description = input("Description (optional): ").strip()
                urgent = _ask_yes_no("Urgent? (y/n): ")
                important = _ask_yes_no("Important? (y/n): ")
                due = input("Due date/time (optional, e.g., DD/MM/YY 14:30): ").strip()
                due_val = due if due else None

                tracker.create_task(
                    title=title,
                    urgent=urgent,
                    important=important,
                    description=description,
                    due_datetime=due_val,
                )
                print("Task created & saved.")

            elif choice == "2":
                _print_tasks_numbered(tracker.list_tasks())

            elif choice == "3":
                q = _ask_int("Quadrant (1-4): ", 1, 4)
                _print_tasks_numbered(tracker.list_tasks_by_quadrant(q))

            elif choice == "4":
                tasks = tracker.list_tasks()
                _print_tasks_numbered(tasks)
                if not tasks:
                    continue
                idx = _ask_int("Task number to mark completed: ", 1, len(tasks))
                tracker.mark_task_completed(idx)
                print("Task marked completed & saved.")

            elif choice == "5":
                tasks = tracker.list_tasks()
                _print_tasks_numbered(tasks)
                if not tasks:
                    continue
                idx = _ask_int("Task number to delete: ", 1, len(tasks))
                tracker.delete_task(idx)
                print("Task deleted & saved.")

            elif choice == "6":
                break
            else:
                print("Invalid option. Try again.")

        except ValueError as e:
            print(f"Error: {e}")


def run_cli() -> None:
    storage = JsonStorage(file_path="data.json")
    tracker = HabitTracker(storage=storage)
    tracker.load()

    while True:
        print("\n=== Habit Tracker (Phase 2) ===")
        print("1) Create habit")
        print("2) List habits (numbered)")
        print("3) List habits by periodicity")
        print("4) Check-off habit (pick by number)")
        print("5) Delete habit (pick by number)")
        print("6) Analytics")
        print("7) Load demo habits (5 habits + 4-week data)")
        print("8) Eisenhower Matrix (tasks)")
        print("9) Exit")

        choice = input("Select an option: ").strip()

        try:
            if choice == "1":
                name = input("Habit name: ").strip()
                description = input("Description (optional): ").strip()
                periodicity = input("Periodicity (daily/weekly): ").strip()
                tracker.create_habit(name=name, description=description, periodicity=periodicity)
                print("Habit created & saved.")

            elif choice == "2":
                _print_habits_numbered(tracker.list_habits())

            elif choice == "3":
                p = input("Periodicity to filter (daily/weekly): ").strip()
                _print_habits_numbered(tracker.list_habits_by_periodicity(p))

            elif choice == "4":
                name = _choose_habit(tracker)
                if name is None:
                    continue
                tracker.check_off(name)
                print(f"Habit '{name}' completed & saved.")

            elif choice == "5":
                name = _choose_habit(tracker)
                if name is None:
                    continue
                confirm = _ask_yes_no(f"Delete habit '{name}'? (y/n): ")
                if confirm:
                    tracker.delete_habit(name)
                    print("Habit deleted & saved.")
                else:
                    print("Cancelled.")

            elif choice == "6":
                _analytics_menu(tracker)

            elif choice == "7":
                confirm = _ask_yes_no("This will REPLACE current habits with demo data. Continue? (y/n): ")
                if confirm:
                    tracker.replace_all_habits(build_predefined_habits_with_4_weeks_data())
                    print("Demo data loaded & saved.")
                else:
                    print("Cancelled.")

            elif choice == "8":
                _task_matrix_menu(tracker)

            elif choice == "9":
                tracker.save()
                print("Goodbye!")
                break

            else:
                print("Invalid option. Try again.")

        except ValueError as e:
            print(f"Error: {e}")
