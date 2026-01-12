from habit import Habit
from tabulate import tabulate

class HabitManager:
    """Class provides in-memory storage of habits and methods to load habits from storage,
    list in-memory habits, create and delete habits and get habits by their ID."""

    def __init__(self, storage=None):
        """Initialize a new HabitManager instance with an empty list of habits."""
        self.storage = storage  # Initial dependency to storage object
        self.habits = []        # Create empty in-memory habit list
        self.next_id = 1        # Generate next ID to current maximum ID

    def create_habit(self, name, description, period):
        """
        Create a new habit, add to in memory list, save to db and return it.

        Args:
            name: Habit name (str)
            description: Habit description (str)
            period: "daily" or "weekly" (str)

        Returns:
            returns habit object
        """
        habit = Habit(
            name=name,
            description=description,
            period=period,
            )
        self.habits.append(habit)       # self.habits grows in memory [Habit(id=1),Habit(id=2),NewHabit(id=?)]
        self.storage.save_habit(habit)  # saves habit metadata to database, assigns habit.habit_id
        print(f"Created habit ID is {habit.habit_id}")
        self.next_id += 1

        return habit

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

    def print_habits_table(self):
        """Functional helper: Pretty table using str."""
        table = [[h.habit_id, h.name, h.description, h.period, len(h.completed_dates), h.streak]
                 for h in self.habits]
        print(tabulate(table,
                        headers=["ID","Name", "Description", "Period", "Completions", "Streak"],
                        tablefmt="github",
                        showindex=range(1,len(self.habits)+1)
                        ))
        # Return mapping: {number: habit_id}
        return {i + 1: h.habit_id for i, h in enumerate(self.habits)}

    '''
        def print_habits_table(self):
            """Functional helper: Pretty table using str."""
            table = [[h.name, h.description, h.period, len(h.completed_dates)] for h in self.habits]
            print(tabulate(table,
                            headers=["Name", "Description", "Periodicity", "Completions"],
                            tablefmt="github",
                            showindex=range(1,len(self.habits)+1)
                            ))
            # Return mapping: {number: habit_id}
            return {i + 1: h.habit_id for i, h in enumerate(self.habits)}
    '''