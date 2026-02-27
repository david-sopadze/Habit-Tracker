from habit_tracker.models import Habit


def test_add_completion_adds_timestamp():
    habit = Habit(name="Test Habit", periodicity="daily")
    habit.add_completion()

    assert len(habit.completions) == 1
