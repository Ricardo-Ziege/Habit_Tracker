import questionary
from tabulate import tabulate
from analysis import list_all_habits, list_habit_by_period, longest_streak_of_all, longest_streak_one
from habit_manager import HabitManager
from db import DatabaseStorage
from sample_data import setup_sample_data

def main_loop():
    """The command line interface provides an interactive menu. It reads and translates user choices."""

    questionary.print("Welcome To Your Habit Tracking App!", style="bold fg:blue")

    # Initialize new session
    storage = DatabaseStorage()         # Create storage object and initialize database
    manager = HabitManager(storage)     # Create manager object and hand-over storage object

    # Load existing habits and next_id from the database on startup
    manager.habits, manager.next_id = storage.load_all_habits() or []

    # Load sample habits if database returns empty list
    if not manager.habits:
        questionary.print("No Habits Found! Run Your Demo With 5 Predefined Habits!", style="bold fg:red")
        setup_sample_data(manager)

    # Show CLI till user exits
    stop = False
    while not stop:
        # Start with interactive menu and initial choices
        choice = questionary.select(
            "How Can I Help You Today?",
            choices=["List Your Habits",
                     "Complete A Habit",
                     "Create A New Habit",
                     "Delete A Habit",
                     "Analyze Your Habits",
                     "Exit"]
        ).ask()


        # Translates user choices to manager functionalities
        if choice == "List Your Habits":
            if manager.habits:
                manager.print_habits_table()
            else:
                print("No habits to display.")


        elif choice == "Complete A Habit":
            if manager.habits:
                num_id_mapping = manager.print_habits_table()   # Prints table and gets number-ID mapping
                try:
                    number = int(questionary.text("Enter habit number to complete:",
                                              validate=lambda x: x.isdigit()).ask())
                    habit_id = num_id_mapping.get(number)
                    if habit_id:
                        habit = manager.get_habit((habit_id))
                        habit.complete_habit()
                        manager.storage.save_habit(habit)
                        print(f"Habit {habit.name} is completed today!")
                        print(f"New streak is {habit.streak}. Keep it going!")
                    else:
                        print(f"Habit number not found.")
                except ValueError:
                    print(f"Enter a valid number.")
            else: print(f"No habits to complete.")


        elif choice == "Create A New Habit":
            name = questionary.text("What's the name of your habit?").ask()
            description = questionary.text("What's the description?").ask()
            periodicity = questionary.select("And periodicity?",choices=["daily","weekly"]).ask()
            if periodicity == "daily": period = "daily"
            elif periodicity == "weekly": period = "weekly"

            habit = manager.create_habit(name, description, period)


            print(f" ID: {habit.habit_id} Created: '{habit.name}'")
            print(f" Desc: {habit.description}, Period: {habit.period}")


        elif choice == "Delete A Habit":
            if manager.habits:
                num_id_mapping = manager.print_habits_table()  # Prints table and gets number-ID mapping
                try:
                    number = int(questionary.text("Enter Habit Number To Delete:",
                                              validate=lambda x: x.isdigit()).ask())
                    habit_id = num_id_mapping.get(number)
                    if habit_id:
                        manager.delete_habit(habit_id)
                        print(f" Deleted habit number {number}")
                    else:
                        print("Habit number not found.")
                except ValueError:
                    print("Enter valid ID.")
            else:
                print("No habits to delete.")


        elif choice == "Analyze Your Habits":
            if manager.habits:
                analyse = questionary.select("Analyze Your Habits",
                                             choices=["List Your Habits",
                                                      "List Your Habits By Periodicity",
                                                      "Calculate Longest Streak Of All Habits",
                                                      "Calculate Longest Streak Of Single Habit"]).ask()
                if analyse == "List Your Habits":
                    print(list_all_habits(manager.habits))
                elif analyse == "List Your Habits By Periodicity":
                    periodicity = questionary.select("For Which Periodicity?", choices=["daily", "weekly"]).ask()
                    print(list_habit_by_period(manager.habits, periodicity))
                elif analyse == "Calculate Longest Streak Of All Habits":
                    print(longest_streak_of_all(manager.habits))
                elif analyse == "Calculate Longest Streak Of Single Habit":
                    num_id_mapping = manager.print_habits_table()
                    number = int(questionary.text("Enter Habit Number To Calculate Streak Of:",
                                                validate=lambda x: x.isdigit()).ask())
                    habit_id = num_id_mapping.get(number)
                    if habit_id:
                        print(longest_streak_one(manager.habits, habit_id))
            else:
                print("No habits to analyze.")


        elif choice == "Exit":
            questionary.print("Have A Good One! See You Tomorrow!", style="bold fg:blue")
            stop = True


if __name__ == "__main__":
    main_loop()
