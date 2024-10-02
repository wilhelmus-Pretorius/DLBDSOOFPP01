# Habit Tracker Application

The Habit Tracker Application provides a system to manage and track daily, weekly, monthly, yearly, and once-off habits effectively. It utilizes a JSON file to persistently store habit data and offers functionalities to add, remove, complete, and analyze habits.

## Setup

To set up the Habit Tracker Application on your local machine, follow these steps:

1. Ensure Python 3.7 or later is installed.
2. Clone or download the repository to your local machine.
3. Navigate to the project directory and install required packages (if any).

## EditHabits Class

### Initialization

- **`__init__(self, file_path)`**:
  - **Description**: Initializes a new instance of the `EditHabits` class, specifying the path to the JSON file used to store habit data.
  - **Parameters**:
    - `file_path`: A string specifying the path to the JSON file.
  - **Usage**:
    ```python
    tracker = EditHabits("path/to/habits.json")
    ```

### Adding Habits

- **`add_uncompleted_habit(self, period, task, time)`**:
  - **Description**: Adds a new habit to the tracker. The habit is initially marked as uncompleted.
  - **Parameters**:
    - `period`: The frequency of the habit ('daily', 'weekly', 'monthly', 'yearly', 'once_off').
    - `task`: The description of the habit.
    - `time`: The time or date when the habit should be completed.
  - **Usage**:
    ```python
    tracker.add_uncompleted_habit('daily', 'Drink Water', '08:00 AM')
    ```

### Removing Habits

- **`remove_uncompleted_habit(self, period, task)`**:
  - **Description**: Removes an uncompleted habit from the tracker.
  - **Parameters**:
    - `period`: The frequency of the habit.
    - `task`: The description of the habit to remove.
  - **Usage**:
    ```python
    tracker.remove_uncompleted_habit('daily', 'Drink Water')
    ```

### Completing Habits

- **`move_to_completed(self, period, task)`**:
  - **Description**: Marks a habit as completed. For recurring habits, it remains in the uncompleted list for future tracking.
  - **Parameters**:
    - `period`: The frequency of the habit.
    - `task`: The description of the habit to complete.
  - **Usage**:
    ```python
    tracker.move_to_completed('weekly', 'Check Emails')
    ```

### Listing and Retrieving Habits

- **`get_tasks_for_day(self, date)`**:
  - **Description**: Retrieves all tasks scheduled for a specific day.
  - **Parameters**:
    - `date`: The specific day in 'YYYY-MM-DD' format.
  - **Usage**:
    ```python
    tasks_today = tracker.get_tasks_for_day('2023-10-03')
    ```

- **`list_all_habits(self)`**:
  - **Description**: Lists all habits stored in the tracker, both completed and uncompleted.
  - **Usage**:
    ```python
    all_habits = tracker.list_all_habits()
    ```

### Analyzing Habits

- **`analyze_habits(self)`**:
  - **Description**: Analyzes all habits to provide insights such as the longest streak and most challenging habits.
  - **Usage**:
    ```python
    habit_analysis = tracker.analyze_habits()
    ```

## Tests

To run tests:

1. Navigate to the project directory.
2. Run `pytest` to execute all tests and verify functionality.
