import pytest
from analysis import list_all_habits, list_habit_by_period, longest_streak_of_all, longest_streak_one
from sample_data import create_sample_habits_and_completions

@pytest.fixture
def habits():
    habits = create_sample_habits_and_completions()
    # Ensure streaks are computed
    for h in habits:
        h.compute_streak()

    # Mock assign IDs for tests
    for i, h in enumerate(habits, start=1):
        h.habit_id = i

    return habits

# Test 1: List all habit names
def test_list_all_habits(habits):
    habit_names = list_all_habits(habits)
    assert habit_names == ["Read", "Play Guitar", "Cook Meal", "Meditate", "Swim"]

# Test 2: List habit names by period
def test_list_habit_by_period_weekly(habits):
    weekly = list_habit_by_period(habits, "weekly")
    assert weekly == ["Meditate", "Swim"]

# Test 3: Calculate longest streak of all sample data
def test_longest_streak_of_all(habits):
    result = longest_streak_of_all(habits)
    assert result == ["Read", 28]

# Test 4: Calculate streak for third habit stored in sample data
def test_longest_streak_one(habits):
    longest = longest_streak_one(habits, 3)
    assert longest == ["Cook Meal", 7]