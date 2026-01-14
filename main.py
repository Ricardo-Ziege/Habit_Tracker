"""
******************
*** CLI Module ***
******************

Provides interactive habit tracking menu (questionary-based).
Main entry point for users: Create, complete, delete, and analyze habits.
Integrates HabitManager (OOP) with handlers (FP-inspired CLI logic).
Persistence via DatabaseStorage (SQLite).

******************
"""


import questionary
from tabulate import tabulate
from habit_manager import HabitManager
from db import DatabaseStorage
from sample_data import setup_sample_data
from handlers import _handle_complete, _handle_create, _handle_delete, _handle_analyze

def main_loop():
    """CLI main loop with interactive menu translating user choices to HabitManager and Analytics."""

    questionary.print("Welcome To Your Habit Tracking App!", style="bold fg:blue")

    # Initialize new session with storage and load stored habits from database
    storage = DatabaseStorage()
    manager = HabitManager(storage)
    manager.habits = storage.load_all_habits()

    # Load demo data if empty (5 predefined habits, 4 weeks of completion data)
    if not manager.habits:
        questionary.print("No Habits Found! Run Your Demo With 5 Predefined Habits!", style="bold fg:red")
        setup_sample_data(manager)

    # Interactive menu loop
    stop = False
    while not stop:
        choice = questionary.select(
            "How Can I Help You Today?",
            choices=["List Your Habits",
                     "Complete A Habit",
                     "Create A New Habit",
                     "Delete A Habit",
                     "Analyze Your Habits",
                     "Exit"]
        ).ask()

        # Translates user choices to handles in handles.py
        if choice == "List Your Habits":
            if manager.habits:
                manager.print_habits_table()
            else:
                print("No habits to display.")

        elif choice == "Complete A Habit":
            _handle_complete(manager)

        elif choice == "Create A New Habit":
            _handle_create(manager)

        elif choice == "Delete A Habit":
            _handle_delete(manager)

        elif choice == "Analyze Your Habits":
            _handle_analyze(manager)

        elif choice == "Exit":
            questionary.print("Have A Good One! See You Tomorrow!", style="bold fg:blue")
            stop = True

if __name__ == "__main__":
    main_loop()
