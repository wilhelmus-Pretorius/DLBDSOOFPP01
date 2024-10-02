import pytest
import sys
from pathlib import Path
import shutil

# Adjust the system path to ensure the main library can be imported
sys.path.append("C:\\Users\\123wi\\OneDrive\\Desktop\\duits uni\\OOP python\\code")

from main_library import EditHabits  # Import the EditHabits class

# Fixture to initialize EditHabits instance with a temporary JSON file for testing
@pytest.fixture(scope="module")
def habit_tracker(tmp_path_factory):
    """
    Creates a temporary habit tracker instance with a new JSON file.
    Ensures each test module uses a separate instance isolated from others.
    """
    temp_file = tmp_path_factory.mktemp("data") / "test_habits.json"
    tracker = EditHabits(str(temp_file))
    tracker.create_empty_habits_file(str(temp_file))  # Initialize an empty habits structure
    return tracker

# Test for adding an uncompleted habit
def test_add_uncompleted_habit(habit_tracker):
    """
    Verifies that an uncompleted habit can be added to the tracker.
    """
    habit_tracker.add_uncompleted_habit('daily', 'Morning Exercise', '07:00')
    assert ['Morning Exercise', '07:00'] in habit_tracker.habit_data['uncompleted_habits']['daily']

# Test for removing an uncompleted habit
def test_remove_uncompleted_habit(habit_tracker):
    """
    Ensures that an uncompleted habit can be removed from the tracker.
    """
    habit_tracker.add_uncompleted_habit('daily', 'Evening Yoga', '18:00')
    habit_tracker.remove_uncompleted_habit('daily', 'Evening Yoga')
    assert ['Evening Yoga', '18:00'] not in habit_tracker.habit_data['uncompleted_habits']['daily']

# Test for moving a habit to completed
def test_move_to_completed(habit_tracker):
    """
    Checks that a habit can be correctly marked as completed and still
    appears in the list of uncompleted habits if it's a recurring type.
    """
    habit_name = 'Check Emails'
    habit_time = 'Monday 09:00'
    habit_tracker.add_uncompleted_habit('weekly', habit_name, habit_time)
    habit_tracker.move_to_completed('weekly', habit_name)

    assert [habit_name, habit_time] in habit_tracker.habit_data['uncompleted_habits']['weekly']
    assert any(habit_name in entry for entry in habit_tracker.habit_data['completed_habits']['weekly'])

# Test for retrieving tasks for a specific day
def test_get_tasks_for_day(habit_tracker):
    """
    Tests if the tracker can correctly retrieve tasks scheduled for a specific day.
    """
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    habit_tracker.add_uncompleted_habit('daily', 'Drink Water', '08:00')
    tasks = habit_tracker.get_tasks_for_day(today)
    assert "Daily: Drink Water at 08:00" in tasks

# Test for listing all habits
def test_list_all_habits(habit_tracker):
    """
    Verifies that all habits, both completed and uncompleted, are correctly listed.
    """
    habit_tracker.add_uncompleted_habit('monthly', 'Pay Bills', '01 12:00')
    habit_tracker.move_to_completed('monthly', 'Pay Bills')
    all_habits = habit_tracker.list_all_habits()

    assert "Uncompleted Monthly: Pay Bills at 01 12:00" in all_habits
    assert "Completed Monthly: Pay Bills at " in ' '.join(h for h in all_habits if "Pay Bills" in h)

# Test for the completion of once-off habits
def test_once_off_habit_completion(habit_tracker):
    """
    Confirms that once-off habits are correctly removed from uncompleted after completion,
    and appear in the completed list.
    """
    habit_name = 'Project Deadline'
    habit_time = '2024-11-01 17:00'
    habit_tracker.add_uncompleted_habit('once_off', habit_name, habit_time)
    habit_tracker.move_to_completed('once_off', habit_name)

    assert [habit_name, habit_time] not in habit_tracker.habit_data['uncompleted_habits']['once_off']
    assert any(habit_name in entry for entry in habit_tracker.habit_data['completed_habits']['once_off'])

# Test for analyzing habits
def test_analyze_habits(habit_tracker):
    """
    Tests the analysis functionality to ensure it provides correct insights
    into the habits' data, such as longest streaks and most challenging habits.
    """
    analysis = habit_tracker.analyze_habits()
    assert analysis['longest_streak']['habit'] is not None
    assert analysis['current_daily_habits'] != []
    assert analysis['most_challenging']['habit'] is not None

# Fixture to clean up the test directory after all tests are run
@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """
    Automatically removes the temporary directory used for tests after all tests are completed.
    Ensures that no residual data affects other tests or clutters the system.
    """
    def remove_test_dir():
        temp_dir = Path(str(request.config._tmpdirhandler.getbasetemp()))
        parent_dir = temp_dir.parent
        if parent_dir.exists():
            shutil.rmtree(parent_dir)  # Removes the directory even if it has contents
    request.addfinalizer(remove_test_dir)
