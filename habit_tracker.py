# Import necessary modules
import json
from datetime import datetime
import logging
import os

# Define the Habit class to represent individual habits
class Habit:
    def __init__(self, name, periodicity):
        # Initialize a new habit with a name, periodicity, creation date, and an empty list for completed tasks
        self.name = name
        self.periodicity = periodicity
        self.created_at = datetime.now()
        self.completed_tasks = []

    def add_completed_task(self):
        # Record the current date and time when a task is completed
        self.completed_tasks.append(datetime.now())

    def __str__(self):
        # Define a string representation of the habit for display purposes
        return f"{self.name} ({self.periodicity})"

# Define the HabitTracker class to manage a list of habits
class HabitTracker:
    def __init__(self):
        # Initialize a HabitTracker with an empty list of habits
        self.habits = []

    def create_habit(self, name, periodicity):
        # Create a new habit and add it to the list of habits
        habit = Habit(name, periodicity)
        self.habits.append(habit)

    def list_habits(self):
        # List all habits and their details
        return [habit.__str__() for habit in self.habits]

    def list_habits_by_periodicity(self, periodicity):
        # List habits with a specific periodicity
        return [habit.__str__() for habit in self.habits if habit.periodicity == periodicity]

    def longest_streak(self, habit_name):
        # Calculate the longest streak of completed tasks for a given habit
        if habit_name not in [habit.name for habit in self.habits]:
            return 0
        streak = 0
        max_streak = 0
        for habit in self.habits:
            if habit.name == habit_name:
                for i in range(len(habit.completed_tasks) - 1):
                    if (habit.completed_tasks[i] - habit.completed_tasks[i+1]).days == -1:
                        streak += 1
                    else:
                        max_streak = max(max_streak, streak)
                        streak = 0
        return max(max_streak, streak)

    def analyze_habits(self):
        # Perform an analysis of all habits, including completed tasks and longest streaks
        analysis = {}
        for habit in self.habits:
            habit_name = habit.name
            analysis[habit_name] = {
                "completed_tasks": len(habit.completed_tasks),
                "longest_streak": self.longest_streak(habit_name)
            }
        return analysis

    def save_to_json(self, filename):
        # Serialize the habit tracker data and save it to a JSON file
        def custom_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            else:
                raise TypeError("Object not serializable")

        data = {
            "habits": [habit.__dict__ for habit in self.habits]
        }
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4, default=custom_serializer)

    def load_from_json(self, filename):
        # Load data from a JSON file and populate the habit tracker
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            self.habits = [Habit(**habit_data) for habit_data in data["habits"]]

# Define a function to load data from a JSON file into a HabitTracker instance
def load_data(filename):
    habit_tracker = HabitTracker()
    
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        
        for habit_data in data.get("habits", []):
            habit = Habit(habit_data["name"], habit_data["periodicity"])
            habit.completed_tasks = [datetime.fromisoformat(task) for task in habit_data["completed_tasks"]]
            habit_tracker.habits.append(habit)
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return habit_tracker

# Define a function to create a habit and save it to the JSON file
def create_habit(name, periodicity, habit_tracker):
    habit_tracker.create_habit(name, periodicity)

    habit_tracker.save_to_json("habits.json")
    print(f"Habit '{name}' created!")

# Define a function to complete a task for a habit and save the changes to the JSON file
def complete_task(habit_name, habit_tracker):
    habit_names = [habit.name for habit in habit_tracker.habits]
    if habit_name not in habit_names:
        raise ValueError(f"Habit '{habit_name}' not found.")
    habit_tracker.habits[habit_names.index(habit_name)].add_completed_task()
    habit_tracker.save_to_json("habits.json")
    print(f"Task completed for habit '{habit_name}'!")

# Define a function to analyze habits and display the results
def analyze_habits(habit_tracker):
    analysis = habit_tracker.analyze_habits()
    print("\nHabit Analysis:")
    for habit_name, data in analysis.items():
        print(f"Habit: {habit_name}")
        print(f"Completed Tasks: {data['completed_tasks']}")
        print(f"Longest Streak: {data['longest_streak']} days")
        print()

# Configure logging
def setup_logging():
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize data and start the main program
def initialize_data(filename):
    habit_tracker = HabitTracker()
    
    # Create some habits and add them to the tracker
    habit_tracker.create_habit("Exercise", "Daily")
    habit_tracker.create_habit("Reading", "Weekly")
    habit_tracker.create_habit("Eating", "Daily")
    habit_tracker.create_habit("Coding", "Daily")
    habit_tracker.create_habit("Praying", "Weekly")

    # Add example tracking data for a period of 4 weeks
    for habit in habit_tracker.habits:
        if habit.periodicity == "Daily":
            for _ in range(28):  # Assuming 4 weeks of daily tracking
                habit.add_completed_task()
        else:  # Assuming "Weekly" periodicity
            for _ in range(4):  # Assuming 4 weeks of weekly tracking
                habit.add_completed_task()
    
    # Save the data to a JSON file
    habit_tracker.save_to_json(filename)

# Main program entry point
def main():
    # Set up logging to record program activity
    setup_logging()
    logging.info('Starting Habit Tracking App')
    
    filename = "habits.json"  # Define the filename for saving habit data
    
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        # Check if a data file exists and is not empty
        # If data exists, load it into the HabitTracker
        habit_tracker = load_data(filename)
    else:
        # If no data file is found, initialize the HabitTracker with sample data
        initialize_data(filename)
        habit_tracker = load_data(filename)
    
    while True:
        print("\nHabit Tracking App Menu:")
        print("1. Create a Habit")
        print("2. List All Habits")
        print("3. List Habits by Periodicity")
        print("4. Complete a Task for a Habit")
        print("5. Analyze Habits")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter habit name: ")
            periodicity = input("Enter periodicity (daily/weekly): ")
            create_habit(name, periodicity, habit_tracker)
        
        elif choice == "2":
            # List all habits in the HabitTracker
            habits = habit_tracker.list_habits()
            print("\nAll Habits:", habits)
        
        elif choice == "3":
            # List habits by a specified periodicity
            periodicity = input("Enter periodicity (daily/weekly): ")
            habits = habit_tracker.list_habits_by_periodicity(periodicity)
            print(f"\nHabits with {periodicity} periodicity:", habits)
        
        elif choice == "4":
            habit_name = input("Enter the name of the habit you completed: ")
            complete_task(habit_name, habit_tracker)
        
        elif choice == "5":
            # Analyze habits and display statistics
            analyze_habits(habit_tracker)
        
        elif choice == "6":
            logging.info('Exiting Habit Tracking App')
            print("Exiting the Habit Tracking App. Goodbye!")
            break

if __name__ == "__main__":
    main()
