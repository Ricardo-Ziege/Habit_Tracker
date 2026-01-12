import pytest
from habit_manager import HabitManager

####################################
### Tests for HabitManager class ###
####################################

# Create MockStorage to prevent writing to DB
class MockStorage:
    def save_habit(self, habit):
        # Assign a fake ID so HabitManager logic works
        if habit.habit_id is None:
            habit.habit_id = 1

    def delete_habit(self, habit_id):
        pass

# Return a manager object with injected MockStorage
@pytest.fixture
def manager():
    return HabitManager(MockStorage())

# Test 1: create_habit() adds to in-memory list
def test_create_habit_adds_to_list(manager):
    habit = manager.create_habit("Read", "Read 15min", "daily")
    assert len(manager.habits) == 1
    assert manager.habits[0].name == "Read"

# Test 2: delete_habit() removes item
def test_delete_habit(manager):
    habit = manager.create_habit("Read", "Read 15min", "daily")
    assert manager.delete_habit(habit.habit_id) is True
    assert manager.get_habit(habit.habit_id) is None

# Test 3: get_habit() returns None if missing
def test_get_habit(manager):
    assert manager.get_habit(99) is None

