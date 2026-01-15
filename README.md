# Habit Tracker App


## What is it?

A command-line habit tracking application built with Object-Oriented and Functional Programming in Python, 
featuring analytics and SQLite persistence.

### Features
- Create and manage habits with daily or weekly periodicity
- Track habit completion and streak calculations
- Functional analytics module providing:
  - List all habits
  - Filter habits by periodicity
  - Calculate historically longest streak over all habits
  - Calculate historically longest streak per habit
- SQLite persistence (habits.db) for reliable data storage across sessions
- Interactive CLI using questionary for intuitive user interaction
- Comprehensive test suite using pytest for Habit, HabitManager, and Analytics modules
- Sample data with 5 predefined habits (daily & weekly) and 4 weeks of completion data

### Architecture
- Habit class (OOP): Encapsulates habit data — habit name, description, periodicity and completion history.
- HabitManager Class (OOP): Manages habit CRUD operations and provides clean API access.
- Analytics Module (FP): Pure functions for aggregating and analyzing habit data without side effects.
- Database: SQLite3 for persistence, handling schema and queries transparently.
- CLI Interface: Interactive menu-driven interface for user interaction.

### Documentation
Code is documented with Python docstrings. Key classes and functions include detailed docstrings
explaining parameters, return values, and usage (Google style).

### Data Storage
Habits and completion data are stored in (habits.db) (SQLite). The database is created automatically on first run.

### Example Data
The application includes 5 predefined habits (3 daily, 2 weekly) with 4 weeks of example completion data for testing 
and validation.

### Requirements
- Python 3.7 or later


## Installation


To install and run the Habit Tracker, follow these steps:

### 1. Clone the Repository

Clone or download the project to your computer using Git:

```shell
git clone https://github.com/Ricardo-Ziege/Habit_Tracker.git
```

### 2. Navigate to the Project Directory

```shell
cd path/to/Habit_Tracker
```

### 3. Create and Activate a Virtual Environment

Creating a virtual environment isolates project dependencies.

#### On Windows:

```shell
python -m venv .venv
.venv\Scripts\activate
```

#### On macOS/Linux:

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Once activated, your command prompt will show `(.venv)` prefix, indicating the virtual environment is active.

### 4. Install Dependencies

Install the required dependencies (third-party libraries) from the `requirements.txt` file:

```shell
pip install -r requirements.txt
```


## Usage 

After installation, you can start running the Habit Tracker in a Terminal window from its root directory with...

```shell
python main.py
```

...and follow the interactive menu to:
- List Your Habits – View all tracked habits in a formatted table
- Complete A Habit – Mark a habit as completed today
- Create A New Habit – Add a new habit with name, description, and periodicity
- Delete A Habit – Remove a habit from tracking
- Analyze Your Habits – View analytics on your habit streaks and patterns
- Exit – Close the application

Find out where to type ??? to discover hidden messages!


## Testing

Run all tests with pytest:

```shell
pytest . 
```

### Test Files

- test_habit.py (4 tests):
    - Habit initialization with period normalization 
    - Daily streak calculation with gap
    - Weekly streak calculation with ISO weeks and gap
    - Habit completion adds date and updates streaks

- test_habit_manager.py (4 tests):
    - Creating habits adds to in-memory list 
    - Deleting habits removes by ID 
    - Listing habits returns correct names 
    - Getting non-existent habit returns None

- test_analytics.py (4 tests):
    - List all habits returns correct names
    - Filter habits by periodicity (weekly/daily)
    - Longest streak of all habits returns max
    - Longest streak of single habit by ID


## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
See [LICENSE](LICENSE) file for details.


## Author

Author:             Ricardo Ziege

Matriculation Nr:   UPS10797871

Task:               Habit Tracker Application

Course:             Object Oriented and Functional Programming With Python (DLBDSOOFPP01)

Further Eduction:   Diploma Data Analytics – Python

Institution:        IU International University - Academy