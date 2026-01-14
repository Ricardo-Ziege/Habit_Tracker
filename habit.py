"""
---------------------
Habit Tracking Module
---------------------
Implements Habit class for completion logging and streak calculation in a Habit Tracker App.
---------------------
"""

from datetime import timedelta, date  # to work with datetime formats import datetime module

class Habit: # Create habit class
    """Models a single habit and logic of habit completion and streak calculation for daily/ weekly habits."""

    def __init__(self, name, description, period, habit_id=None):
        """
        Initializes new habit object.

        Args:
            name (str):                 Habit name.
            description (str):          Habit description.
            period (str):               'daily' or 'weekly' (lowercased).
            habit_id (str, optional):   Unique ID for persistence

        Note:
            Streak starts at 0.
            completed_dates is empty list.
        """
        self.name = name
        self.description = description
        self.period = period.lower()
        self.habit_id = habit_id
        self.longest_streak = 0
        self.current_streak = 0
        self.completed_dates = []

    def complete_habit(self):
        """
        Checks-off a habit as completed today (by default) and update streak.

        Returns:
            bool:   True if newly added
                    False if already completed today
        """
        today = date.today()
        if today not in self.completed_dates:
            self.completed_dates.append(today)
            self.compute_streak()
            return True
        else: return False

    def compute_streak(self):
        """
        Computes current and longest streak based on periodicity ('daily' or 'weekly').

        Note:
            daily:      Consecutive days
            weekly:     Consecutive ISO weeks

            Updates     self.current_streak == longest streak ending at most recent completion
                        self.longest_streak == historically longest streak over all completions
        """
        sorted_dates = sorted(self.completed_dates)
        if not sorted_dates:
            self.streak = 0
            return

        longest_streak = 1
        current_streak = 1

        if self.period == "daily":
            expected_delta = timedelta(days=1)
            for i in range(1, len(sorted_dates)):
                delta = sorted_dates[i] - sorted_dates[i - 1]
                if delta == expected_delta:
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    current_streak = 1


        elif self.period == "weekly":
           prev_week = sorted_dates[0].isocalendar()[1]
           for date in sorted_dates[1:]:
                curr_week = date.isocalendar()[1]
                if curr_week == prev_week + 1:
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    current_streak = 1
                prev_week = curr_week

        self.longest_streak = longest_streak
        self.current_streak = current_streak