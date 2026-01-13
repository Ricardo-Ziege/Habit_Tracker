# Analytics Functional Module
"""This module contains all required analysis functions."""

def list_all_habits(habits):
    """
    List all stored habit names using list comprehension.

    Args:
        habits:     List of habit objects

    Returns:
        List[str]:  List of habit names
    """
    return [h.name for h in habits]

def list_habit_by_period(habits, period):
    """
    List all stored habit names filtered by periodicity and using list comprehension

    Args:
        habits:     List of habit objects
        period:     Periodicity of habit

    Returns:
        List:       List of habit names filtered by periodicity
    """
    return [h.name for h in habits if h.period == period]

def longest_streak_of_all(habits):
    """
    Return the longest streak of all habits

    Args:
        habits:     List of habit objects

    Returns:
        List:       Pair of habit name and longest streak
    """
    if not habits:
        return None
    longest = max(habits, key=lambda h: h.streak)
    return [longest.name, longest.streak]

def longest_streak_one(habits, habit_id):
    """
    Return the longest streak for a single habit
    Args:
        habits:     List of habit objects
        habit_id:   Habit ID
    Returns:
        str, int    Tuple of habit.name and longest streak
    """
    habit = next((h for h in habits if h.habit_id == habit_id), None)
    if habit is None:
        return None
    return [habit.name, habit.streak]
