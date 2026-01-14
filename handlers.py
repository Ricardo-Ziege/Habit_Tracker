"""CLI handler functions for habit operations in CLI in main.py."""

import questionary
from sample_data import print_sample_data
from analysis import list_all_habits, list_habit_by_period, longest_streak_of_all, longest_streak_one

def _handle_complete(manager):
    """Handle habit completion with user-friendly ID mapping."""
    if not manager.habits:
        print("No habits to complete.")
        return
    manager.print_habits_table()
    num_id_mapping = manager.get_display_mapping()
    try:
        number = int(questionary.text("Enter habit number to complete:",
                                      validate=lambda x: x.isdigit()).ask())
        habit_id = num_id_mapping.get(number)
        if habit_id:
            habit = manager.get_habit(habit_id)
            if habit.complete_habit():
                print(f"Great! Habit {habit.name} is successfully completed today.")
                print(f"New streak is {habit.current_streak}. Keep it going!")
            else:
                print(f"Habit {habit.name} was already completed today.")
            manager.storage.save_habit(habit)
        else:
            print("Enter a valid number.")
    except ValueError:
        print("Enter a valid number.")


def _handle_create(manager):
    """Prompt and create new habit interactively."""
    name = questionary.text("What's the name of your new habit?",
                            validate=lambda x: len(x.strip()) > 0 or 'Type habit name').ask()
    while True:
        desc = questionary.text("What do you need to do to complete it?",
                                validate=lambda x: len(x.strip()) > 0 or "Type habit description or ???").ask()
        if desc.strip() == "???":
            print_sample_data()
        else:
            break
    period = questionary.select("And how often you plan to do it?",
                                choices=["daily", "weekly"]).ask()
    habit = manager.create_habit(name, desc, period)
    print(f"Your new habit '{habit.name}' is created today!")
    print(f"{habit.description} {habit.period} to complete it and come back.")


def _handle_delete(manager):
    """Handle habit deletion with ID mapping."""
    if not manager.habits:
        print("No habits to delete.")
        return
    manager.print_habits_table()
    num_id_mapping = manager.get_display_mapping()
    try:
        number = int(questionary.text("Enter The Habit Number To Delete:",
                                      validate=lambda x: x.isdigit()).ask())
        habit_id = num_id_mapping.get(number)
        if habit_id:
            manager.delete_habit(habit_id)
            print(f"Your Habit at position {number} was deleted.")
        else:
            print("Enter a valid number.")
    except ValueError:
        print("Enter a valid number.")


def _handle_analyze(manager):
    """Handle analytics sub-menu with functional calls."""
    if not manager.habits:
        print("No habits to analyze.")
        return
    analyse = questionary.select("Analyze Your Habits",
                                 choices=["List Your Habits",
                                          "List Your Habits By Periodicity",
                                          "Calculate Longest Historical Streak Of All Habits",
                                          "Calculate Longest Historical Streak Of A Single Habit"]).ask()

    if analyse == "List Your Habits":
        habit_names = list_all_habits(manager.habits)
        habit_text = ", ".join(habit_names)
        print(f"\nYou are currently tracking the habits {habit_text}. That's impressive!\n")

    elif analyse == "List Your Habits By Periodicity":
        periodicity = questionary.select("For Which Periodicity?", choices=["daily", "weekly"]).ask()
        habit_names = list_habit_by_period(manager.habits, periodicity)
        habit_text = ", ".join(habit_names)
        print(f"\nYour habits {habit_text} are to be completed {periodicity}.\n")

    elif analyse == "Calculate Longest Historical Streak Of All Habits":
        longest = longest_streak_of_all(manager.habits)
        if longest is None:
            print("No habits to analyze.")
        else:
            print(f"\nYour longest historical streak is {longest[1]} completions in a row with the habit {longest[0]}. "
                  f"Keep it up!\n")

    elif analyse == "Calculate Longest Historical Streak Of A Single Habit":
        manager.print_habits_table()
        num_id_mapping = manager.get_display_mapping()
        try:
            number = int(questionary.text("Enter Habit Number To Calculate Streak Of:",
                                          validate=lambda x: x.isdigit()).ask())
            habit_id = num_id_mapping.get(number)
            if habit_id:
                longest = longest_streak_one(manager.habits, habit_id)
                if longest:
                    print(f"\nYour longest historical streak for {longest[0]} was {longest[1]} times in a row. "
                          f"Carry on!\n")
                else:
                    print("Habit not found.")
            else:
                print("Enter a valid number.")
        except ValueError:
            print("Enter a valid number.")