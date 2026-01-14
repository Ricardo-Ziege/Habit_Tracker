"""
-------------------------------
Unit tests for Analytics module
-------------------------------
"""

import pytest
from analysis import list_all_habits, list_habit_by_period, longest_streak_of_all, longest_streak_one
from sample_data import create_sample_habits_and_completions

@pytest.fixture
def habits():
    """Create sample habits with computed streaks and mock IDs for testing."""
    habits = create_sample_habits_and_completions()
    # Compute streaks from completion data
    for h in habits:
        h.compute_streak()
    # Assign mock IDs for tests
    for i, h in enumerate(habits, start=1):
        h.habit_id = i

    return habits

def test_list_all_habits(habits):
    """Test 1: list_all_habits() returns all habit names in order."""
    habit_names = list_all_habits(habits)
    assert habit_names == ["Read", "Play Guitar", "Cook Meal", "Meditate", "Swim"]
    assert len(habit_names) == 5

def test_list_habit_by_period(habits):
    """Test 2: list_habit_by_period() filters by 'weekly' period."""
    weekly = list_habit_by_period(habits, "weekly")
    assert weekly == ["Meditate", "Swim"]
    assert len(weekly) == 2

def test_longest_streak_of_all(habits):
    """Test longest_streak_of_all() returns historically longest streak of all habits."""
    result = longest_streak_of_all(habits)
    assert result == ["Read", 20]

# Test 4: Calculate streak for third habit stored in sample data
def test_longest_streak_one(habits):
    """Test longest_streak_one() returns historically longest streak for specific habit by ID."""
    longest = longest_streak_one(habits, 3)
    assert longest == ["Cook Meal", 7]