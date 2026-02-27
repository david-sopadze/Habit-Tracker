from habit_tracker.fixtures import build_predefined_habits_with_4_weeks_data


def test_fixtures_create_five_habits():
    habits = build_predefined_habits_with_4_weeks_data()
    assert len(habits) == 5
    assert any(h.periodicity == "daily" for h in habits)
    assert any(h.periodicity == "weekly" for h in habits)
