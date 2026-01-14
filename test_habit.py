"""
--------------------------
Unit Tests for Habit Class
--------------------------
"""

import pytest
from datetime import date
from habit import Habit

def test_habit_creation():
    """Test 1: Habit initialization with all attributes and period normalization."""
    habit = Habit("Habit", "Description", "Daily", 24)
    assert habit.name == "Habit"
    assert habit.description == "Description"
    assert habit.period == "daily"
    assert habit.habit_id == 24
    assert habit.current_streak == 0
    assert habit.longest_streak == 0
    assert habit.completed_dates == []

def test_streak_calc_daily():
    """Test 2: Daily current and longest streaks - consecutive days, breaks on +1 day gap."""
    habit = Habit("Habit","Description", "Daily")
    habit.completed_dates = [date(2025, 12, 10),
                             date(2025, 12, 11),
                             date(2025, 12, 13)]
    habit.compute_streak()
    assert habit.current_streak == 1
    assert habit.longest_streak == 2    # Consecutive 10-11.12, breaks at 13.12

def test_streak_calc_weekly():
    """Test 2: Daily current and longest streaks - consecutive ISO weeks, breaks on +1 ISO week gap."""
    habit = Habit("Habit","Description", "Weekly")
    habit.completed_dates = [date(2026, 1, 1),      # ISO week 1: current = 1; longest = 1
                             date(2026, 1, 8),      # ISO week 2: current = 2; longest = 2
                             date(2026, 1, 19),     # ISO week 4: current = 1; longest = 2
                             date(2026, 1, 26)]     # ISO week 5: current = 2; longest = 2
    habit.compute_streak()
    assert habit.current_streak == 2
    assert habit.longest_streak == 2

def test_habit_completion():
    """Test 4: complete_habit adds today and triggers streak recompute."""
    habit = Habit("Habit","Description", "Weekly")
    habit.completed_dates = [date(2025, 12, 10),
                             date(2025, 12, 11),
                             date(2025, 12, 13)
                             ]
    habit.complete_habit()
    assert habit.completed_dates[-1] == date.today()
    assert habit.current_streak > 0