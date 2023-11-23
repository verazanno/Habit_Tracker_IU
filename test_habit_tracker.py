import unittest
from habit_tracker import HabitTracker, Habit, create_habit, complete_task, analyze_habits, load_data

class TestHabitTracker(unittest.TestCase):
    def setUp(self):
        self.habit_tracker = HabitTracker()

    def test_create_habit(self):
        # Test creating a habit
        create_habit("Test Habit", "daily", self.habit_tracker)
        self.assertEqual(len(self.habit_tracker.habits), 1)

    def test_list_habits(self):
        # Test listing habits
        self.habit_tracker.habits.append(Habit("Test Habit", "daily"))
        habits = self.habit_tracker.list_habits()
        self.assertIn("Test Habit (daily)", habits)

    def test_list_habits_by_periodicity(self):
        # Test listing habits by periodicity
        self.habit_tracker.habits.append(Habit("Test Habit", "daily"))
        habits = self.habit_tracker.list_habits_by_periodicity("daily")
        self.assertIn("Test Habit (daily)", habits)

    def test_longest_streak(self):
        # Test calculating the longest streak for a habit
        habit = Habit("Test Habit", "daily")
        habit.add_completed_task()
        habit.add_completed_task()
        self.habit_tracker.habits.append(habit)
        streak = self.habit_tracker.longest_streak("Test Habit")
        self.assertEqual(streak, 1)  # Updated to 1

    def test_analyze_habits(self):
        # Test analyzing habits
        self.habit_tracker.habits.append(Habit("Test Habit", "daily"))
        analysis = self.habit_tracker.analyze_habits()
        self.assertIn("Test Habit", analysis)

    def test_invalid_habit_name(self):
        # Test completing a task for a non-existent habit
        with self.assertRaises(ValueError):  # Expecting a ValueError
            complete_task("Non-Existent Habit", self.habit_tracker)

    def test_load_data(self):
        # Test loading data from a file
        initial_habit_tracker = self.habit_tracker
        # Save the habit tracker to a file
        initial_habit_tracker.save_to_json("test_habits.json")
        # Load the habit tracker from the file
        loaded_habit_tracker = load_data("test_habits.json")
        # Check if the loaded habit tracker is equal to the initial one
        self.assertEqual(loaded_habit_tracker.habits, initial_habit_tracker.habits)

if __name__ == '__main__':
    unittest.main()
