"""
----------------
Analytics Module
----------------
Implements functional habit analysis.

Pure functions using list comprehensions, max(), next() for:
- Listing habits (all/ filtered by periodicity))
- Streak computations (all/ single habit)

Expects list of Habit objects.
----------------
"""

def list_all_habits(habits):
    """
    Lists all stored habit names using list comprehension.

    Args:
        habits (list [Habit]):  List of Habit objects

    Returns:
        list [str]:             List of habit names
    """
    return [h.name for h in habits]

def list_habit_by_period(habits, period):
    """
    List habit names filtered by periodicity using list comprehension.

    Args:
        habits (list [Habit]):  List of Habit objects
        period (str):           'daily' or 'weekly'

    Returns:
        list [str]:             List of matching habit names
    """
    return [h.name for h in habits if h.period == period]

def longest_streak_of_all(habits):
    """
    Find habit with longest historical streak across all habits.

    Args:
        habits (list [Habit]):  List of Habit objects.

    Returns:
        list [str, int]:        [habit_name, streak] of maximum or
                                None if empty.
    """
    if not habits:
        return None
    habit = max(habits, key=lambda h: h.longest_streak)
    return [habit.name, habit.longest_streak]

def longest_streak_one(habits, habit_id):
    """
    Get longest historical streak for a single habit by ID.

    Args:
        habits (list [Habit]):  List of Habit objects
        habit_id (str):         Unique habit ID

    Returns:
        list [str, int]:        [habit_name, streak] or
                                None if not found
    """
    habit = next((h for h in habits if h.habit_id == habit_id), None)
    if habit is None:
        return None
    return [habit.name, habit.longest_streak]
