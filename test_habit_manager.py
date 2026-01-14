"""
---------------------------------
Unit Tests for HabitManager class
---------------------------------
"""

import pytest
from habit_manager import HabitManager

class MockStorage:
    """Mock storage backend to prevent DB writes during testing."""
    def save_habit(self, habit):
        """Assign fake ID if new habit."""
        if habit.habit_id is None:
            habit.habit_id = 1

    def delete_habit(self, habit_id):
        pass

@pytest.fixture
def manager():
    """HabitManager with mock storage."""
    return HabitManager(MockStorage())

def test_create_habit_adds_to_list(manager):
    """Test 1: create_habit() adds new habit to in-memory list."""
    habit = manager.create_habit("Read","Read for 15min.","daily")
    assert len(manager.habits) == 1
    assert manager.habits[0].name == "Read"
    assert habit.habit_id is not None  # Storage assigned ID

def test_delete_habit_runs(manager):
    """Test 2: delete_habit() removes habit by ID."""
    habit = manager.create_habit("Read","Read for 15min.","daily")
    assert manager.delete_habit(habit.habit_id) is True
    assert manager.get_habit(habit.habit_id) is None

def test_list_habits_returns_names(manager):
    """Test list_habits returns all habit names."""
    manager.create_habit("Read","Read for 15min.","daily")
    manager.create_habit("Play Guitar","Practice for 10min.", "daily")
    names = manager.list_habits()
    assert names == ["Read", "Play Guitar"]

def test_get_habit(manager):
    """Test 3: get_habit() returns None for non-existent ID."""
    assert manager.get_habit(99) is None

