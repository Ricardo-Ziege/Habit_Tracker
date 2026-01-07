from habit import Habit
from db import DatabaseStorage

class HabitManager:
    """Class provides in-memory storage of habits and methods to load habits from storage,
    list in-memory habits, create and delete habits and get habits by their ID."""

    def __init__(self, storage=None):
        """Initialize a new HabitManager instance with an empty list of habits."""
        # Constructor injection
        self.storage = storage # initial dependency to storage instance
        self.habits = [] # and in-memory habit list
        self.next_id = 1 # Generate unique habit ID

    def create_habit(self, name, description, period):
        """
        Create a new habit, add to in memory list, save to db and return it.

        Args:
            name: Habit name (str)
            description: Habit description (str)
            period: "daily" or "weekly" (str)

        Returns:
            returns habit instance
        """
        habit = Habit(
            name=name,
            description=description,
            period=period,
            )
        self.habits.append(habit)       # self.habits grows [Habit(id=1),Habit(id=2)]
        self.storage.save_habit(habit)  # gets habid_id from save_habit function
        print(f"Created habit ID {habit.habit_id}")
        self.next_id += 1

        return habit

    def load_habits(self):
        """Load from storage, update next_id."""
        self.habits = self.storage.load_all_habits()
        if self.habits:
            self.next_id = max(habit.habit_id for habit in self.habits) + 1
        else:
            self.next_id = 1

    def save_habits(self):
        """Save all in-memory habits (before exit)."""
        for habit in self.habits:
            self.storage.save_habit(habit)

    def list_habits(self):
        """Return list of all habit names from in-memory storage."""
        return [habit.name for habit in self.habits]

    def delete_habit(self, habit_id):
        """
        Delete one habit by ID from in-memory list and storage.

        Args:
            habit_id: ID of habit to delete

        Returns:
            True if deleted, False if not found.
        """
        for i, habit in enumerate(self.habits):
            if habit.habit_id == habit_id:
                del self.habits[i]
                self.storage.delete_habit(habit_id)
                return True
        return False

    def get_habit(self, habit_id):
        """
        Get one habit by ID from in-memory list.

        Args:
            habit_id: ID of habit to get

        Returns:
            returns habit if found, None if not found.
        """
        for habit in self.habits:
            if habit.habit_id == habit_id:
                return habit
        return None