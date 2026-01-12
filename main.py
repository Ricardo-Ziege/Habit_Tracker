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
            name = questionary.text("What's the name of your new habit?").ask()
            description = questionary.text("What do you need to do to complete it?").ask()
            periodicity = questionary.select("And how often you plan to do it?",choices=["daily","weekly"]).ask()
            if periodicity == "daily": period = "daily"
            elif periodicity == "weekly": period = "weekly"

            habit = manager.create_habit(name, description, period)

            print(f" Your new habit '{habit.name}' is created today!")
            print(f" {habit.description} {habit.period} to complete it and come back.")


        elif choice == "Delete A Habit":
            if manager.habits:
                num_id_mapping = manager.print_habits_table()  # Prints table and gets number-ID mapping
                try:
                    number = int(questionary.text("Enter The Habit Number To Delete:",
                                              validate=lambda x: x.isdigit()).ask())
                    habit_id = num_id_mapping.get(number)
                    if habit_id:
                        manager.delete_habit(habit_id)
                        print(f" Your Habit at position {number} was deleted.")
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
                    print(f"Your longest streak is {longest[1]} completed with the habit {longest[0]}. Keep it up!")

                elif analyse == "Calculate Longest Streak Of A Single Habit":
                    num_id_mapping = manager.print_habits_table()
                    number = int(questionary.text("Enter Habit Number To Calculate Streak Of:",
                                                validate=lambda x: x.isdigit()).ask())
                    habit_id = num_id_mapping.get(number)
                    if habit_id:
                        streak = longest_streak_one(manager.habits, habit_id)
                        habit = next((h for h in manager.habits if h.habit_id == habit_id), None)
                        if habit:
                            print(f"Your habit {habit.name} was completed {streak} consecutively. Carry on!")
                        else:
                            print("Habit not found.")
                    else:
                        print("Invalid habit number.")

            else:
                print("No habits to analyze.")

        elif choice == "Exit":
            questionary.print("Have A Good One! See You Tomorrow!", style="bold fg:blue")
            stop = True


if __name__ == "__main__":
    main_loop()
