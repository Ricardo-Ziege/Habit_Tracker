import questionary
from tabulate import tabulate
from analysis import list_all_habits, list_habit_by_period, longest_streak_of_all, longest_streak_one
from habit_manager import HabitManager
from db import DatabaseStorage
from sample_data import setup_sample_data, print_sample_data


def main_loop():
    """The command line interface provides an interactive menu. It reads and translates user choices."""

    questionary.print("Welcome To Your Habit Tracking App!", style="bold fg:blue")

    # Initialize new session
    storage = DatabaseStorage()         # Create storage object and initialize database
    manager = HabitManager(storage)     # Create manager object and hand-over storage object

    # Load existing habits and next_id from the database on startup
    manager.habits = storage.load_all_habits()

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
                manager.print_habits_table()                    # Prints formatted table
                num_id_mapping = manager.get_display_mapping()  # Gets number-ID mapping
                try:
                    number = int(questionary.text("Enter habit number to complete:",
                                              validate=lambda x: x.isdigit()).ask())
                    habit_id = num_id_mapping.get(number)
                    if habit_id:
                        habit = manager.get_habit((habit_id))
                        if habit.complete_habit():
                            print(f"Great! Habit {habit.name} is successfully completed today.")
                            print(f"New streak is {habit.streak}. Keep it going!")
                        else:
                            print(f"Habit {habit.name} was already completed today.")
                        manager.storage.save_habit(habit)
                    else:
                        print(f"Enter a valid number.")
                except ValueError:
                    print(f"Enter a valid number.")
            else: print(f"No habits to complete.")


        elif choice == "Create A New Habit":
            name = questionary.text("What's the name of your new habit?",
                                    validate=lambda x: len(x.strip()) > 0 or 'Type habit name.').ask()
            while True:
                desc = questionary.text("What do you need to do to complete it?",
                                    validate=lambda x: len(x.strip()) > 0 or "Type habit description or ???").ask()
                if desc.strip()== "???": print_sample_data()
                else: break
            period = questionary.select("And how often you plan to do it?",
                                    choices=["daily","weekly"]).ask()

            habit = manager.create_habit(name, desc, period)

            print(f" Your new habit '{habit.name}' is created today!")
            print(f" {habit.description} {habit.period} to complete it and come back.")


        elif choice == "Delete A Habit":
            if manager.habits:
                manager.print_habits_table()                    # Prints formatted table
                num_id_mapping = manager.get_display_mapping()  # Gets number-ID mapping
                try:
                    number = int(questionary.text("Enter The Habit Number To Delete:",
                                              validate=lambda x: x.isdigit()).ask())
                    habit_id = num_id_mapping.get(number)
                    if habit_id:
                        manager.delete_habit(habit_id)
                        print(f" Your Habit at position {number} was deleted.")
                    else:
                        print(f"Enter a valid number.")
                except ValueError:
                    print(f"Enter a valid number.")
            else:
                print("No habits to delete.")


        elif choice == "Analyze Your Habits":
            if manager.habits:
                analyse = questionary.select("Analyze Your Habits",
                                             choices=["List Your Habits",
                                                      "List Your Habits By Periodicity",
                                                      "Calculate Longest Streak Of All Habits",
                                                      "Calculate Longest Streak Of A Single Habit"]).ask()

                if analyse == "List Your Habits":
                    habit_names = list_all_habits(manager.habits)
                    habit_text = ", ".join(habit_names)
                    print(f"You are currently tracking the habits {habit_text}. That's impressive!")


                elif analyse == "List Your Habits By Periodicity":
                    periodicity = questionary.select("For Which Periodicity?", choices=["daily", "weekly"]).ask()
                    habit_names = list_habit_by_period(manager.habits, periodicity)
                    habit_text = ", ".join(habit_names)
                    print(f"Your habits {habit_text} are to be completed {periodicity}.")

                elif analyse == "Calculate Longest Streak Of All Habits":
                    longest = longest_streak_of_all(manager.habits)
                    if longest is None:
                        print("No habits to analyze.")
                    else:
                        print(f"Your longest streak is {longest[1]} completions in a row with the habit {longest[0]}. "
                          f"Keep it up!")

                elif analyse == "Calculate Longest Streak Of A Single Habit":
                    manager.print_habits_table()                    # Prints formatted table
                    num_id_mapping = manager.get_display_mapping()  # Gets number-ID mapping
                    try:
                        number = int(questionary.text("Enter Habit Number To Calculate Streak Of:",
                                                    validate=lambda x: x.isdigit()).ask())
                        habit_id = num_id_mapping.get(number)
                        if habit_id:
                            longest = longest_streak_one(manager.habits, habit_id)
                            if longest:
                                print(f"Your habit {longest[0]} was completed {longest[1]} times in a row. Carry on!")
                            else:
                                print("Habit not found.")
                        else:
                            print(f"Enter a valid number.")
                    except ValueError:
                        print(f"Enter a valid number.")

            else:
                print("No habits to analyze.")

        elif choice == "Exit":
            questionary.print("Have A Good One! See You Tomorrow!", style="bold fg:blue")
            stop = True


if __name__ == "__main__":
    main_loop()
