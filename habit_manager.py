"""
--------------------
Habit Manager Module
--------------------
Implements HabitManager class for in-memory habit storage and CRUD operations.
Manages list of Habit objects, integrates with storage backend, provides table display for Habit Tracker App.
--------------------
"""

from habit import Habit
from tabulate import tabulate

class HabitManager:
    """Provides in-memory storage of habits with methods to create, list, delete and retrieve by ID."""

    def __init__(self, storage=None):
        """Initializes new HabitManager object with empty habits list and optional storage.

        Args:
            storage:    Storage backend for persistence (DB)
        """
        self.storage = storage  # Initial dependency to storage object
        self.habits = []

    def create_habit(self, name, description, period):
        """
        Creates new Habit object, add to in-memory list, save to storage and return it.

        Args:
            name (str):         Habit name.
            description (str):  Habit description.
            period (str):       'daily' or 'weekly'.

        Returns:
            Habit:              New Habit object with assigned ID from storage.
        """
        habit = Habit(
            name=name,
            description=description,
            period=period,
            )
        self.habits.append(habit)
        self.storage.save_habit(habit)

        return habit

    def list_habits(self):
        """Returns list of all habit names from in-memory storage."""
        return [habit.name for habit in self.habits]

    def delete_habit(self, habit_id):
        """
        Deletes habit by ID from in-memory list and storage.

        Args:
            habit_id:   ID of habit to delete.

        Returns:
            bool:       True if deleted
                        False if not found
        """
        for i, habit in enumerate(self.habits):
            if habit.habit_id == habit_id:
                del self.habits[i]
                self.storage.delete_habit(habit_id)
                return True
        return False

    def get_habit(self, habit_id):
        """
        Retrieves habit by ID from in-memory list.

        Args:
            habit_id:   ID of habit to get.

        Returns:
            Habit:      Habit if found
                        None if not found
        """
        for habit in self.habits:
            if habit.habit_id == habit_id:
                return habit
        return None

    def print_habits_table(self):
        """Prints formatted overview table with row indices using tabulate."""
        table = [[h.name, h.description, h.period, h.current_streak] for h in self.habits]
        print(tabulate(table,
                        headers=["Name", "Description", "Periodicity", "Current Streak"],
                        tablefmt="github",
                        showindex=range(1,len(self.habits)+1)
                        ))
                        
    def get_display_mapping(self):
        """Return mapping of display numbers (1-based) to internal habit IDs."""
        return {i + 1: h.habit_id for i, h in enumerate(self.habits)}

    '''
    FOR DEBUGGING:
        def print_habits_table(self):
            """Prints formatted overview table using tabulate with row indices."""
            table = [[h.habit_id, h.name, h.description, h.period, len(h.completed_dates), h.current_streak, h.longest_streak]
                     for h in self.habits]
            print(tabulate(table,
                            headers=["ID","Name", "Description", "Period", "Completions", "Current Streak", "Longest Streak"],
                            tablefmt="github",
                            showindex=range(1,len(self.habits)+1)
                            ))

        def get_display_mapping(self):
            """Return mapping of display numbers (1-based) to internal habit IDs."""
            return {i + 1: h.habit_id for i, h in enumerate(self.habits)}
    '''

