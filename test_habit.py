import pytest
from datetime import date
from habit import Habit

#############################
### Tests for Habit class ###
#############################

# Test 1: Habit creation
def test_habit_creation():
    habit = Habit("Habit", "Description", "Daily", 24)
    assert habit.name == "Habit"
    assert habit.description == "Description"
    assert habit.period == "daily"  # gets converted to lowercase
    assert habit.habit_id == 24
    assert habit.streak == 0

# Test 2: Daily habit completion + reset
def test_streak_calc_daily():
    habit = Habit("Habit","Description", "Daily")
    habit.completed_dates = [date(2025, 12, 10),
                             date(2025, 12, 11),
                             date(2025, 12, 13)]
    habit.compute_streak()
    assert habit.streak == 2  # Streak calculation works for consecutive dates and breaks after 1 day gap

# Test 3: Weekly habit completion + reset
def test_streak_calc_weekly():
    habit = Habit("Habit","Description", "Weekly")
    habit.completed_dates = [date(2025, 12, 1),
                             date(2025, 12, 8),
                             date(2025, 12, 15),
                             date(2025, 12, 22),
                             date(2025, 12, 29)]
    habit.compute_streak()
    assert habit.streak == 5

# Test 4: Habit completion
def test_habit_completion():
    habit = Habit("Habit","Description", "Weekly")
    habit.completed_dates = [date(2025, 12, 10),
                             date(2025, 12, 23),
                             date(2025, 12, 24)
                             ]
    habit.complete_habit()
    assert habit.completed_dates[-1] == date.today()
