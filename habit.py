from datetime import timedelta, date  # to work with datetime formats import datetime module

class Habit: # Create habit class
    """Class determines single habit attributes and logic of habit completion and streak calculation."""

    def __init__(self, name, description, period, habit_id=None): # initialize new instance with 3 attributes name, description and period
        self.name = name
        self.description = description
        self.period = period.lower() # 'daily' or 'weekly'
        self.habit_id = habit_id
        self.streak = 0 # create new attribute streak, starting value = 0
        self.completed_dates = [] # create empty list --> fill with date objects

    # PERFORM METHODS
    def complete_habit(self):
        """Check off the habit as completed on a given date with today by default and updates streak."""
        today = date.today()
        if today not in self.completed_dates:
            self.completed_dates.append(today) # add new date entry to completed_dates list
            self.compute_streak()

    def compute_streak(self):
        """Compute longest streak based on periodicity ("daily" or "weekly")."""
        sorted_dates = sorted(self.completed_dates)
        if not sorted_dates:
            self.streak = 0
            return

        longest_streak = 1
        current_streak = 1
        expected_delta = timedelta(days=1) if self.period == "daily" else timedelta(days=7)

        for i in range(1, len(sorted_dates)):
            if sorted_dates[i] - sorted_dates[i - 1] == expected_delta:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1

        self.streak = longest_streak

    def get_streak(self):
        """Returns current streak as an integer."""
        return self.streak

