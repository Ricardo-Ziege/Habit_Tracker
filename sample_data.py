from datetime import timedelta, date
from habit import Habit

def create_sample_habits_and_completions():
    """Create sample habits and completions data for testing streak calculation."""
    habit1 = Habit("Read","Read for 15min.","daily")
    habit2 = Habit("Play Guitar","Practice for 10min.", "daily")
    habit3 = Habit("Cook Meal","Prepare a healthy meal for yourself and others", "daily")
    habit4 = Habit("Meditate","Meditate for 20min.", "weekly")
    habit5 = Habit( "Swim","Swim for 60min.", "weekly")

    # Generate completion dates
    today = date.today()

    # Habit1 (daily): 28 consecutive days
    habit1.completed_dates = [today - timedelta(days=i) for i in range(28, 0, -1)]

    # Habit2 (daily): alternate daily (14 completions, streak 1)
    habit2.completed_dates = [today - timedelta(days=i) for i in range(27, 0, -1) if i % 2 == 1]

    # Habit3 (daily): 7 on, 7 off, 7 on, 7 off (14 completions, streak 7)
    habit3.completed_dates = []
    habit3.completed_dates.extend([today - timedelta(days=i) for i in range(7, 0, -1)])  # Days 1-7
    habit3.completed_dates.extend([today - timedelta(days=i) for i in range(21, 14, -1)])  # Days 15-21
    habit3.completed_dates = sorted(habit3.completed_dates)

    # Habit4 (weekly): alternate weekly (2 random completions in week 1 and 3, streak 1)
    habit4.completed_dates = [today - timedelta(weeks=3), today - timedelta(weeks=1)]

    # Habit5 (weekly): 4 consecutive weeks (4 completions, streak 4)
    habit5.completed_dates = [today - timedelta(weeks=3), today - timedelta(weeks=2),
              today - timedelta(weeks=1), today]

    # return habit3.completed_dates
    return [habit1, habit2, habit3, habit4, habit5]

def setup_sample_data(manager):
    """Setup sample data like real data: create habits, save to database, reload with IDs and compute streaks."""
    habits = create_sample_habits_and_completions()

    for habit in habits:
        habit.compute_streak()              # Compute and persist streaks in habit objects
        manager.storage.save_habit(habit)   # Creates ID's, saves metadata and completions
        manager.habits.append(habit)        # Add to in-memory list