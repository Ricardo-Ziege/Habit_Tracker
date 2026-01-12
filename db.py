import sqlite3
from habit import Habit
from datetime import datetime as dt

class DatabaseStorage:
    """Class establishes a database connection and enables loading and saving of habit data."""

    # Specifiy a database name
    _db_name = 'habits.db'  # _db_name is a protected attribute

    # Initialize a new DatabaseStorage instance
    def __init__(self):
        self._initialize_db()

    def _initialize_db(self):
        """
        Initialize the database connection. Give SQL code instructions.
        Create two tables, named habits and completions, for static and dynamic data.
        """
        with sqlite3.connect(self._db_name) as conn:  # context manager, benefit of auto-closing
            cursor = conn.cursor()
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS habits
                           (
                               habit_id INTEGER PRIMARY KEY,
                               name TEXT NOT NULL,
                               description TEXT NOT NULL,
                               period TEXT NOT NULL
                           )
                           """)
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS completions
                           (
                               id INTEGER PRIMARY KEY,
                               habit_id INTEGER,
                               completed_dates TEXT,
                               FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
                           )
                           """)
            conn.commit()

    def save_habit(self, habit):  # Saves current state of a habit to database
        """Saves a habit to the database."""
        with sqlite3.connect(self._db_name) as conn:
            cursor = conn.cursor()

            # Save static metadata
            if habit.habit_id:
                # Update existing habit metadata in habits table
                cursor.execute("""
                               UPDATE habits
                               SET name = ?, description = ?,period = ?
                               WHERE habit_id = ?
                               """, (habit.name, habit.description, habit.period, habit.habit_id))
            else:
                # Insert new habit metadata into habits table
                cursor.execute("""
                               INSERT INTO habits (name, description, period)
                               VALUES (?, ?, ?)
                               """, (habit.name, habit.description, habit.period))
                habit.habit_id = int(cursor.lastrowid) # writes new habit.habit_id as last row of habits table
                print("DEBUG lastrowid after INSERT:", cursor.lastrowid)

            # Save dynamic tracking data
            # Get existing completions for this habit
            cursor.execute("""
                           SELECT completed_dates
                           FROM completions
                           WHERE habit_id = ?
                           """, (habit.habit_id,))
            existing_dates = {row[0] for row in cursor.fetchall()}

            # Insert new completions that don't already exist in the database
            for d in habit.completed_dates:
                date = d.isoformat()
                if date not in existing_dates:
                    cursor.execute("""
                                   INSERT into completions (habit_id, completed_dates)
                                   VALUES (?, ?)
                                   """, (habit.habit_id, date))
            conn.commit()

    # LOADING FROM DATABASE
    @classmethod
    def load_habit(cls, habit_id): # Habit retrieval by its ID from storage
        """Retrieve a single habit by its ID along with its tracking data from storage."""
        with sqlite3.connect(cls._db_name) as conn:
            cursor = conn.cursor()

            # Fetch habit metadata
            cursor.execute("""
                SELECT name, description, period, habit_id FROM habits WHERE habit_id = ?
            """, (habit_id,))
            result = cursor.fetchone()
            if not result:
                return None
            name, description, period, habit_id = result

            habit = Habit(name=result[0], description=result[1], period=result[2], habit_id=int(result[3]))

            # Fetch habit completions
            cursor.execute("""
                SELECT completed_dates FROM completions WHERE habit_id = ?
            """, (habit_id,))

            habit.completed_dates = [dt.fromisoformat(row[0]).date() for row in cursor.fetchall()]

            return habit

    def load_habit_ids(self):
        """Get all habit IDs for loading all habits from the database."""
        with sqlite3.connect(self._db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT habit_id FROM habits")
            return [(row[0]) for row in cursor.fetchall()]

    def load_all_habits(self):
        """Load habits by ID + recompute streaks + return next_id info."""
        ids = self.load_habit_ids()
        habits = []
        max_id = 0
        for habit_id in ids:
            habit = self.load_habit(habit_id)
            if habit:
                habit.compute_streak()  # Recompute streak here
                habits.append(habit)    # Create new in-memory habits list
                max_id = max(max_id, habit.habit_id)  # Calculate maximum ID from stored habits

        # Return tuple: habits + next_id
        return habits, max_id + 1

    def delete_habit(self, habit_id):
        """
        Delete habit by ID from both tables.

        Args:
            habit_id: int ID of habit to delete

        Returns:
            bool: True if deleted, False if not found
        """
        with sqlite3.connect(self._db_name) as conn:
            cursor = conn.cursor()

            # Verify exists first
            cursor.execute("SELECT habit_id FROM habits WHERE habit_id = ?", (habit_id,))
            if not cursor.fetchone():
                return False

            # Delete completions first
            cursor.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
            print(f"Deleted {cursor.rowcount} completions")  # DEBUG

            # Delete habit
            cursor.execute("DELETE FROM habits WHERE habit_id = ?", (habit_id,))
            print(f"Deleted habit {habit_id}, rowcount: {cursor.rowcount}")  # DEBUG

            conn.commit()
            return True