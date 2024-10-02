import json
from datetime import datetime, timedelta
import os

class EditHabits:


    def __init__(self, file_path):
        """
        Initialize the class with the path to the JSON file.
        If the file does not exist, create it with empty habit data.
        :param file_path: Path to the JSON file containing the habit data.
        """
        self.file_path = file_path
        self.expected_periods = ["daily", "weekly", "monthly", "yearly", "once_off"]
        # Check if the file exists; if not, create an empty habit file
        if not os.path.exists(file_path):
            self.create_empty_habits_file(file_path)
        # Load the habit data after ensuring the file exists
        self.habit_data = self.load_habit_data()


    def create_empty_habits_file(self, new_file_path):
        """
        Generate a new JSON file with empty 'uncompleted_habits', 'completed_habits', and 'history' dictionaries.
        :param new_file_path: The name or path of the new JSON file to create.
        """
        empty_data = {
            "uncompleted_habits": {
                "daily": [],
                "weekly": [],
                "monthly": [],
                "yearly": [],
                "once_off": []
            },
            "completed_habits": {
                "daily": [],
                "weekly": [],
                "monthly": [],
                "yearly": [],
                "once_off": []
            },
            "history": {}  # To store history of when habits were created and completed
        }
        with open(new_file_path, 'w') as new_file:
            json.dump(empty_data, new_file, indent=4)
        print(f"New empty habit file created: {new_file_path}")


    def load_habit_data(self):
        """
        Load and return the habit data dictionary from the specified JSON file.
        :return: Dictionary containing the habit data.
        """
        try:
            with open(self.file_path, 'r') as file:
                habit_data = json.load(file)
            return habit_data
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {self.file_path}")
            return {}


    def save_habit_data(self):
        """
        Save the habit data dictionary to the specified JSON file.
        """
        with open(self.file_path, 'w') as file:
            json.dump(self.habit_data, file, indent=4)
        print(f"Habit data saved to {self.file_path}")


    def add_uncompleted_habit(self, period, task, time):
        """
        Add an uncompleted habit to the habit data and log its creation time.
        :param period: The period of the habit (daily, weekly, etc.).
        :param task: The description of the habit task.
        :param time: The time format for the habit based on the period.
        """
        if period in self.habit_data.get("uncompleted_habits", {}):
            self.habit_data["uncompleted_habits"][period].append([task, time])
            
            # Log creation time in history
            if task not in self.habit_data.get("history", {}):
                self.habit_data["history"][task] = {
                    "created": str(datetime.now()),
                    "completed": [],
                    "removed": None  # Placeholder for removal time
                }
            
            self.save_habit_data()
            print(f"Added new habit '{task}' to {period} habits.")
        else:
            print("Invalid period! Please choose from daily, weekly, monthly, yearly, once_off.")


    def remove_uncompleted_habit(self, period, task):
        """
        Remove an uncompleted habit from the habit data and log its removal time.
        :param period: The period of the habit (daily, weekly, etc.).
        :param task: The description of the habit task to be removed.
        """
        if period in self.habit_data.get("uncompleted_habits", {}):
            for habit in self.habit_data["uncompleted_habits"][period]:
                if habit[0] == task:
                    self.habit_data["uncompleted_habits"][period].remove(habit)

                    # Log removal time in history
                    if task in self.habit_data.get("history", {}):
                        self.habit_data["history"][task]["removed"] = str(datetime.now())
                    else:
                        self.habit_data["history"][task] = {
                            "created": None,
                            "completed": [],
                            "removed": str(datetime.now())
                        }
                    
                    self.save_habit_data()
                    print(f"Removed habit '{task}' from {period} habits.")
                    return
            print(f"Habit '{task}' not found in {period} habits.")
        else:
            print("Invalid period! Please choose from daily, weekly, monthly, yearly, once_off.")


    def move_to_completed(self, period, task):
        """
        Move a habit from uncompleted_habits to completed_habits and log its completion time.
        For recurring habits (daily, weekly, monthly, yearly), do not remove them from uncompleted_habits.
        For once_off habits, remove them from uncompleted_habits after marking as completed.
        :param period: The period of the habit (daily, weekly, etc.).
        :param task: The description of the habit task to be moved.
        """
        if period in self.habit_data.get("uncompleted_habits", {}) and period in self.habit_data.get("completed_habits", {}):
            for habit in self.habit_data["uncompleted_habits"][period]:
                if habit[0] == task:
                    # Add to completed habits with current timestamp
                    completion_time = str(datetime.now())
                    self.habit_data["completed_habits"][period].append([task, completion_time])
                    
                    # Log completion time in history
                    if task in self.habit_data.get("history", {}):
                        self.habit_data["history"][task]["completed"].append(completion_time)
                    else:
                        self.habit_data["history"][task] = {"created": None, "completed": [completion_time], "removed": None}
                    
                    # Only remove from uncompleted habits if it's a once_off task
                    if period == "once_off":
                        self.habit_data["uncompleted_habits"][period].remove(habit)
                        print(f"Removed once-off habit '{task}' from uncompleted {period} habits.")
                    
                    # Save updated habit data back to the file
                    self.save_habit_data()
                    print(f"Marked habit '{task}' as completed in {period} habits.")
                    return
            print(f"Habit '{task}' not found in {period} uncompleted habits.")
        else:
            print("Invalid period! Please choose from daily, weekly, monthly, yearly, once_off.")


    def get_tasks_for_day(self, date):
        """
        Get all tasks scheduled for a specific date.
        :param date: The date in the format 'YYYY-MM-DD'.
        :return: List of tasks scheduled for that day.
        """
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD'.")
            return []

        tasks_for_day = []

        # Daily Habits
        daily_habits = self.habit_data.get("uncompleted_habits", {}).get("daily", [])
        for habit in daily_habits:
            tasks_for_day.append(f"Daily: {habit[0]} at {habit[1]}")

        # Weekly Habits
        weekly_habits = self.habit_data.get("uncompleted_habits", {}).get("weekly", [])
        day_of_week = target_date.strftime("%A")  # e.g., 'Monday'
        for habit in weekly_habits:
            if day_of_week in habit[1]:
                tasks_for_day.append(f"Weekly: {habit[0]} at {habit[1]}")

        # Monthly Habits
        monthly_habits = self.habit_data.get("uncompleted_habits", {}).get("monthly", [])
        day_of_month = target_date.strftime("%d")  # e.g., '15'
        for habit in monthly_habits:
            if habit[1].startswith(day_of_month):
                tasks_for_day.append(f"Monthly: {habit[0]} at {habit[1]}")

        # Yearly Habits
        yearly_habits = self.habit_data.get("uncompleted_habits", {}).get("yearly", [])
        month_day = target_date.strftime("%m-%d")  # e.g., '10-15'
        for habit in yearly_habits:
            if habit[1].startswith(month_day):
                tasks_for_day.append(f"Yearly: {habit[0]} at {habit[1]}")

        # Once-off Habits
        once_off_habits = self.habit_data.get("uncompleted_habits", {}).get("once_off", [])
        for habit in once_off_habits:
            if habit[1].startswith(date):
                tasks_for_day.append(f"Once-off: {habit[0]} at {habit[1]}")

        return tasks_for_day

    def list_all_habits(self):
        """
        Return a list of all tracked habits (completed and uncompleted).
        """
        all_habits = []
        for period, habits in self.habit_data.get("uncompleted_habits", {}).items():
            for habit in habits:
                all_habits.append(f"Uncompleted {period.capitalize()}: {habit[0]} at {habit[1]}")
        for period, habits in self.habit_data.get("completed_habits", {}).items():
            for habit in habits:
                all_habits.append(f"Completed {period.capitalize()}: {habit[0]} at {habit[1]}")
        return all_habits


    def setup_predefined_habits(self):
        """
        Set up the predefined habits for all periods: daily, weekly, monthly, yearly, and once_off.
        Log the creation time for each habit in the history.
        Simulate example tracking data for a period of 4 weeks.
        """
        predefined_habits = {
            "daily": [
                ["Morning Exercise", "07:00"],
                ["Evening Reading", "20:00"]
            ],
            "weekly": [
                ["Weekly Meeting", "Monday 09:00"],
                ["Grocery Shopping", "Saturday 10:00"]
            ],
            "monthly": [
                ["Pay Rent", "01 09:00"],
                ["Team Meeting", "15 11:00"]
            ],
            "yearly": [
                ["Annual Review", "12-31 10:00"],
                ["Doctor Checkup", "06-15 14:00"]
            ],
            "once_off": [
                ["Project Deadline", "2024-11-01 17:00"],
                ["Friend's Wedding", "2024-12-15 16:00"]
            ]
        }
        
        # Add predefined habits to uncompleted habits with history tracking
        for period, habits in predefined_habits.items():
            for habit in habits:
                task, time = habit
                self.habit_data["uncompleted_habits"][period].append([task, time])
                
                # Log creation time in history
                if task not in self.habit_data.get("history", {}):
                    self.habit_data["history"][task] = {
                        "created": str(datetime.now()),  # Log the current time as the creation time
                        "completed": [],
                        "removed": None  # Placeholder for removal time if needed
                    }
        
        # Simulate example tracking data for a period of 4 weeks
        current_date = datetime.now().date()
        
        for task, details in self.habit_data["history"].items():
            # Generate completion dates for each habit
            if "Morning Exercise" in task or "Evening Reading" in task:
                # Simulate daily habits
                for i in range(28):  # 4 weeks of daily data
                    completion_date = current_date - timedelta(days=(28 - i))
                    completion_time = datetime.combine(completion_date, datetime.strptime("07:00" if "Morning Exercise" in task else "20:00", "%H:%M").time())
                    details["completed"].append(completion_time.strftime("%Y-%m-%d %H:%M:%S.%f"))

            elif "Weekly Meeting" in task or "Grocery Shopping" in task:
                # Simulate weekly habits (4 times)
                for i in range(4):
                    completion_date = current_date - timedelta(days=(4 - i) * 7)  # Once a week for 4 weeks
                    completion_time = datetime.combine(completion_date, datetime.strptime("09:00" if "Weekly Meeting" in task else "10:00", "%H:%M").time())
                    details["completed"].append(completion_time.strftime("%Y-%m-%d %H:%M:%S.%f"))

            elif "Pay Rent" in task or "Team Meeting" in task:
                # Simulate monthly habits (1 time in the last 4 weeks)
                completion_date = current_date - timedelta(days=15)  # 15 days ago
                completion_time = datetime.combine(completion_date, datetime.strptime("09:00" if "Pay Rent" in task else "11:00", "%H:%M").time())
                details["completed"].append(completion_time.strftime("%Y-%m-%d %H:%M:%S.%f"))

            elif "Annual Review" in task or "Doctor Checkup" in task:
                # Simulate yearly habits (not completed in the last 4 weeks)
                details["completed"].append("2023-12-31 10:00:00.000000")

        self.save_habit_data()
        print("Predefined habits and example tracking data have been set up for daily, weekly, monthly, yearly, and once_off tasks.")



    def add_completed_habit(self, period, task, completion_time):
        """
        Manually add a completed habit to the completed habits list and log its completion time in history.
        :param period: The period of the habit (daily, weekly, etc.).
        :param task: The description of the habit task.
        :param completion_time: The time the task was completed, format 'YYYY-MM-DD HH:MM'.
        """
        if period in self.habit_data.get("completed_habits", {}):
            self.habit_data["completed_habits"][period].append([task, completion_time])
            
            # Log the completion time in history
            if task in self.habit_data.get("history", {}):
                self.habit_data["history"][task]["completed"].append(completion_time)
            else:
                self.habit_data["history"][task] = {
                    "created": None,
                    "completed": [completion_time],
                    "removed": None
                }
            
            self.save_habit_data()
            print(f"Manually added completed habit '{task}' to {period} habits.")
        else:
            print("Invalid period! Please choose from daily, weekly, monthly, yearly, once_off.")


    def remove_completed_habit(self, period, task):
        """
        Remove a completed habit from the completed habits list and log the removal time in history.
        :param period: The period of the habit (daily, weekly, etc.).
        :param task: The description of the habit task to be removed.
        """
        if period in self.habit_data.get("completed_habits", {}):
            for habit in self.habit_data["completed_habits"][period]:
                if habit[0] == task:
                    self.habit_data["completed_habits"][period].remove(habit)
                    
                    # Log the removal time in history
                    if task in self.habit_data.get("history", {}):
                        self.habit_data["history"][task]["removed"] = str(datetime.now())
                    else:
                        self.habit_data["history"][task] = {
                            "created": None,
                            "completed": [],
                            "removed": str(datetime.now())
                        }
                    
                    self.save_habit_data()
                    print(f"Removed completed habit '{task}' from {period} habits.")
                    return
            print(f"Completed habit '{task}' not found in {period} habits.")
        else:
            print("Invalid period! Please choose from daily, weekly, monthly, yearly, once_off.")


    def edit_uncompleted_habit(self, period, old_task, new_task=None, new_time=None):
        """
        Edit an existing uncompleted habit in the habit data.
        :param period: The period of the habit (daily, weekly, etc.).
        :param old_task: The current task description of the habit.
        :param new_task: The new task description (optional).
        :param new_time: The new time for the habit (optional).
        """
        if period in self.habit_data.get("uncompleted_habits", {}):
            for habit in self.habit_data["uncompleted_habits"][period]:
                if habit[0] == old_task:
                    if new_task:
                        habit[0] = new_task
                    if new_time:
                        habit[1] = new_time
                    self.save_habit_data()
                    print(f"Edited habit '{old_task}' in {period} habits.")
                    return
            print(f"Habit '{old_task}' not found in {period} habits.")
        else:
            print("Invalid period! Please choose from daily, weekly, monthly, yearly, once_off.")


    def analyze_habits(self):
        """
        Analyze habits based on the entire history to determine streaks, current daily habits, and most challenging habits.
        :return: Dictionary with analysis results for habit streaks, current daily habits, and challenging habits.
        """
        # Initialize analysis results
        analysis = {
            "longest_streak": {"habit": None, "streak_length": 0},
            "current_daily_habits": [],
            "most_challenging": {"habit": None, "missed_count": 0}
        }

        # Track longest streaks and most challenging habits
        longest_streak = 0
        most_challenging_count = 0

        # Dictionary to hold habit streaks
        habit_streaks = {}

        # Calculate the current date
        today = datetime.now().date()

        # Analyzing habit history for streaks and challenges
        for task, details in self.habit_data.get("history", {}).items():
            # Calculate streaks based on completion dates
            completed_dates = [
                datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f").date()
                for date in details.get("completed", [])
            ]
            completed_dates.sort()  # Sort the dates to analyze streaks

            # Track habit streaks
            current_streak = 0
            max_streak = 0
            last_date = None

            for date in completed_dates:
                if last_date and date == last_date + timedelta(days=1):
                    current_streak += 1
                else:
                    current_streak = 1
                last_date = date
                max_streak = max(max_streak, current_streak)

            # Update the habit streaks dictionary
            habit_streaks[task] = max_streak

            # Update the longest streak in the analysis if necessary
            if max_streak > longest_streak:
                longest_streak = max_streak
                analysis["longest_streak"] = {"habit": task, "streak_length": longest_streak}

            # Calculate missed counts for the last month
            missed_count = len(details.get("completed", []))  # Assuming each missing count represents a missed day for daily habits

            # Update most challenging habit based on missed counts
            if missed_count > most_challenging_count:
                most_challenging_count = missed_count
                analysis["most_challenging"] = {"habit": task, "missed_count": missed_count}

        # Identify current daily habits that need to be completed (today's uncompleted daily habits)
        current_daily_habits = self.habit_data.get("uncompleted_habits", {}).get("daily", [])
        for habit in current_daily_habits:
            analysis["current_daily_habits"].append(f"{habit[0]} at {habit[1]}")

        return analysis


def main():
    while True:
        # Prompt the user to input a folder path for storing the habit data
        folder_path = input(
            "Enter the folder path to create the habit JSON file.\n"
            "Please use single backslashes (\\) without additional quotes.\n"
            "Example: C:\\Users\\YourName\\Documents\\Folder_name\n"
            "Please enter the folder path: "
        ).strip()

        # Check if the entered folder path exists
        if os.path.isdir(folder_path):
            break  # Exit loop if the folder exists
        else:
            print(f"Folder '{folder_path}' does not exist or is not accessible. Please check the path and try again.\n")

    # Set the full path for the habit file
    file_path = os.path.join(folder_path, "habits.json")
    print(f"Using the following path for habit data: {file_path}")

    # Create the habits.json file if it does not exist
    if not os.path.exists(file_path):
        try:
            with open(file_path, 'w') as file:
                json.dump({
                    "uncompleted_habits": {
                        "daily": [],
                        "weekly": [],
                        "monthly": [],
                        "yearly": [],
                        "once_off": []
                    },
                    "completed_habits": {
                        "daily": [],
                        "weekly": [],
                        "monthly": [],
                        "yearly": [],
                        "once_off": []
                    },
                    "history": {}
                }, file, indent=4)
            print(f"New habits JSON file created at {file_path}")
        except Exception as e:
            print(f"Error creating file at '{file_path}': {e}")
            return
    else:
        print(f"Using existing file at {file_path}")

    # Create an instance of EditHabits with the specified JSON file
    habit_manager = EditHabits(file_path)
    habit_manager.setup_predefined_habits()

    # Display available options
    print("Welcome to the Habit Tracker!")
    print("Available commands:")
    print("1. Add Uncompleted Habit")
    print("2. Remove Uncompleted Habit")
    print("3. Complete a Habit")
    print("4. Add Completed Habit Manually")
    print("5. Remove Completed Habit")
    print("6. List All Habits")
    print("7. Get Tasks for a Specific Day")
    print("8. Analyze Habits")
    print("9. Clean up and Delete Habit File")
    print("10. Exit")

    while True:
        command = input("\nEnter a command number (1-10): ").strip()

        if command == '1':
            period = input("Enter the period (daily, weekly, monthly, yearly, once_off): ").strip().lower()
            task = input("Enter the habit task description: ").strip()
            time = input("Enter the time for the habit (e.g., '07:00' for daily): ").strip()
            habit_manager.add_uncompleted_habit(period, task, time)

        elif command == '2':
            period = input("Enter the period of the habit to remove (daily, weekly, etc.): ").strip().lower()
            task = input("Enter the task description to remove: ").strip()
            habit_manager.remove_uncompleted_habit(period, task)

        elif command == '3':
            period = input("Enter the period of the habit to complete (daily, weekly, etc.): ").strip().lower()
            task = input("Enter the task description to complete: ").strip()
            habit_manager.move_to_completed(period, task)

        elif command == '4':
            period = input("Enter the period of the habit (daily, weekly, etc.): ").strip().lower()
            task = input("Enter the habit task description to add as completed: ").strip()
            completion_time = input("Enter the completion time (YYYY-MM-DD HH:MM): ").strip()
            habit_manager.add_completed_habit(period, task, completion_time)

        elif command == '5':
            period = input("Enter the period of the completed habit to remove (daily, weekly, etc.): ").strip().lower()
            task = input("Enter the task description to remove from completed habits: ").strip()
            habit_manager.remove_completed_habit(period, task)

        elif command == '6':
            print("\n--- All Tracked Habits ---")
            habits = habit_manager.list_all_habits()
            for habit in habits:
                print(habit)

        elif command == '7':
            date = input("Enter the date (YYYY-MM-DD): ").strip()
            tasks = habit_manager.get_tasks_for_day(date)
            print(f"\n--- Tasks for {date} ---")
            for task in tasks:
                print(task)

        elif command == '8':
            analysis = habit_manager.analyze_habits()
            print("\n--- Habit Analysis ---")
            print(f"Longest Streak: {analysis['longest_streak']['habit']} ({analysis['longest_streak']['streak_length']} days)")
            print("Current Daily Habits:")
            for habit in analysis['current_daily_habits']:
                print(f"  - {habit}")
            print(f"Most Challenging Habit: {analysis['most_challenging']['habit']} (Missed {analysis['most_challenging']['missed_count']} times)")

        elif command == '9':
            print("Deleting the habit file to clean up and exit...")
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"File '{file_path}' deleted successfully. Exiting now.")
            else:
                print(f"File '{file_path}' not found for deletion.")
            return  # Exit the program after cleanup

        elif command == '10':
            print("Exiting the Habit Tracker. Goodbye!")
            break

        else:
            print("Invalid command. Please enter a number between 1 and 10.")

if __name__ == "__main__":
    main()


