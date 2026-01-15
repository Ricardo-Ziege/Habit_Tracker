"""
------------------
Sample Data Module
------------------
Creates realistic habits and completions for streak validation.
Used for demo/test fixtures (5 habits, 4 weeks completion data).
Used by CLI on first run or when all habits are deleted from storage or habits.db is deleted.
Contains easter egg, find out where to type '???'
------------------
"""

from datetime import timedelta, date
from habit import Habit
import random

def create_sample_habits_and_completions(today=None):
    """
    Creates sample habits and completions data for testing streak calculation.

    Args:
        today (date, optional):     Reference date for completions
                                    Defaults to date.today()

    Returns:
        list[Habit]:                5 habits with varied streaks (daily/weekly).
    """
    habit1 = Habit("Read","Read for 15min.","daily")
    habit2 = Habit("Play Guitar","Practice for 10min.", "daily")
    habit3 = Habit("Cook Meal","Prepare a healthy meal", "daily")
    habit4 = Habit("Meditate","Meditate for 20min.", "weekly")
    habit5 = Habit( "Swim","Swim for 60min.", "weekly")

    # Generate completion dates relative to today or specified argument today(other date)
    if today is None:
        today = date.today()

    # Habit1 (daily): 28 consecutive days - 1 day
    habit1.completed_dates = [today - timedelta(days=i) for i in range(28, 0, -1)]
    del habit1.completed_dates[20]

    # Habit2 (daily): alternate daily (14 completions, streak 1)
    habit2.completed_dates = [today - timedelta(days=i) for i in range(27, 0, -1) if i % 2 == 1]

    # Habit3 (daily): 7 on, 7 off, 7 on, 7 off (14 completions, streak 7)
    habit3.completed_dates = []
    habit3.completed_dates.extend([today - timedelta(days=i) for i in range(7, 0, -1)])  # Days 1-7
    habit3.completed_dates.extend([today - timedelta(days=i) for i in range(21, 14, -1)])  # Days 15-21
    habit3.completed_dates = sorted(habit3.completed_dates)

    # Habit4 (weekly): alternate weekly (2 completions in week 1 and 3, streak 1)
    habit4.completed_dates = [today - timedelta(weeks=3), today - timedelta(weeks=1)]

    # Habit5 (weekly): 4 consecutive weeks (4 completions, streak 4)
    habit5.completed_dates = [today - timedelta(weeks=3), today - timedelta(weeks=2),
              today - timedelta(weeks=1), today]

    return [habit1, habit2, habit3, habit4, habit5]

def setup_sample_data(manager):
    """
    Load sample data into manager:  Create, compute streaks, persist to DB and add to memory.

    Args:
        manager (HabitManager):     Manager with storage to populate.

    Note:
        Simulates real workflow:    Saves, creates IDs, reload computes streaks.
    """
    habits = create_sample_habits_and_completions()

    for habit in habits:
        habit.compute_streak()
        manager.storage.save_habit(habit)
        manager.habits.append(habit)

























































































































































def print_sample_data():
    messages = [
        "🎭 Aha! A fan of mysteries, I see! But I need WORDS, not question marks!",
        "🤔 Three question marks walk into a habit tracker... Tell me what you really need to do for this habit!",
        "❓❓❓ Very cryptic! But my computer brain needs an actual description. Help a bot out?",
        "🕵️ I see you're going for maximum ambiguity. But seriously, what's the habit?",
        "🥚 Nice try! But mystery habits won't track themselves. Be a good egg!",
        "❌ Nope! No cryptic entries allowed here. What's your habit actually about?",
        "🔮 Ooh, mysterious! But even fortune tellers need more than question marks. Describe it!",
        "🤐 I see you're being coy... but I need actual words to track your progress!",
        "⚡ Plot twist: This app doesn't accept mystery habits. So what's your habit really about?",
        "🎯 Nice try sneaking past me! But every habit deserves a proper description. Lay it on me!",
    ]
    print("\n" + random.choice(messages) + "\n")

