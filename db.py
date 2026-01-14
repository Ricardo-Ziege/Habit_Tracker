"""
-----------------------
Database Storage Module
-----------------------
Implements DatabaseStorage class, used for SQLite persistence of habit and completion data.
Splits static habit data (habits table) and dynamic tracking data (completions table).
Integrates with HabitManager for CRUD operations in habit tracker.
-----------------------
"""

import sqlite3
from habit import Habit
from datetime import datetime as dt

class DatabaseStorage:
    """Establishes database connection and handles loading/saving of habit data."""

    _db_name = 'habits.db'  # _db_name is a protected database name

    def __init__(self):
        """Initializes new DatabaseStorage object and creates tables."""
        self._initialize_db()

    def _initialize_db(self):
        """
        Initializes database tables habits (static) and completions (dynamic) by SQL instructions.

        Uses context manager for auto-closing connection.
        """
        with sqlite3.connect(self._db_name) as conn:
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
        """Saves current habit state to database (static metadata + dynamic completions)."""
        with sqlite3.connect(self._db_name) as conn:
            cursor = conn.cursor()

            # Saves/updates static metadata
            if habit.habit_id:
                cursor.execute("""
                               UPDATE habits
                               SET name = ?, description = ?,period = ?
                               WHERE habit_id = ?
                               """, (habit.name, habit.description, habit.period, habit.habit_id))
            else:
                cursor.execute("""
                               INSERT INTO habits (name, description, period)
                               VALUES (?, ?, ?)
                               """, (habit.name, habit.description, habit.period))
                habit.habit_id = int(cursor.lastrowid) # writes new habit.habit_id as last row of habits table

            # Sync completions (insert new only)
            cursor.execute("""
                           SELECT completed_dates
                           FROM completions
                           WHERE habit_id = ?
                           """, (habit.habit_id,))
            existing_dates = {row[0] for row in cursor.fetchall()}

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
        """Retrieves single habit by ID with completions and metadata."""
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
        """Gets all habit IDs from database."""
        with sqlite3.connect(self._db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT habit_id FROM habits")
            return [(row[0]) for row in cursor.fetchall()]

    def load_all_habits(self):
        """Loads all habits, populate completions, and recompute streaks."""
        ids = self.load_habit_ids()
        habits = []
        for habit_id in ids:
            habit = self.load_habit(habit_id)
            if habit:
                habit.compute_streak()  # Recompute streak here
                habits.append(habit)    # Create new in-memory habits list

        return habits

    def delete_habit(self, habit_id):
        """
        Deletes habit by ID from both tables (completions first).

        Args:
            habit_id (int):     ID of habit to delete

        Returns:
            bool:               True if deleted
                                False if not found
        """
        with sqlite3.connect(self._db_name) as conn:
            cursor = conn.cursor()

            # Verify exists first
            cursor.execute("SELECT habit_id FROM habits WHERE habit_id = ?", (habit_id,))
            if not cursor.fetchone():
                return False

            # Deletes completions first
            cursor.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))

            # Deletes habit
            cursor.execute("DELETE FROM habits WHERE habit_id = ?", (habit_id,))

            conn.commit()
            return True