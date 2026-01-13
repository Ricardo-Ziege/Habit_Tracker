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
            return True
        else: return False

    def compute_streak(self):
        """Compute longest streak based on periodicity ("daily" or "weekly")."""
        sorted_dates = sorted(self.completed_dates)
        if not sorted_dates:
            self.streak = 0
            return

        longest_streak = 1      # Best streak so far
        current_streak = 1      # Streak ending at recent completion

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
            min_delta = timedelta(days=7)
            max_delta = timedelta(days=14)
            for i in range(1, len(sorted_dates)):
                delta = sorted_dates[i] - sorted_dates[i - 1]
                # Accept any date difference inclusive to 7 and exclusive to 14 days to continue streak
                if min_delta <= delta < max_delta:
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)    # Historical maximum
                else:
                    current_streak = 1

        self.streak = longest_streak

