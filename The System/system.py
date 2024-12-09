import tkinter as tk
from tkinter import messagebox, simpledialog  # Include simpledialog here
import random
import pickle
import os
import datetime

class User:
    def __init__(self):
        self.stats = {
            'Strength': 0,
            'Stamina': 0,
            'Agility': 0,
            'Intelligence': 0,
            'Discipline': 0,
            'Willpower': 0
        }
        self.level = 1
        self.quests = []
        self.completed_quests = []
        self.last_login = datetime.datetime.now()

    def generate_quests(self):
        activities = ['Gym', 'Study for 1 hour', 'Jog 21 mins', 'solve puzzles', 'meditate for 10 mins', 'plan your day']
        stats = ['Strength', 'Agility', 'Stamina', 'Intelligence', 'Willpower', 'Discipline']
        self.quests = random.sample(list(zip(activities, stats)), 4)
        self.completed_quests = []

    def update_level(self):
        total_stats = sum(self.stats.values())
        self.level = int((total_stats / 6) / 10) + 1

    def complete_quest(self, quest_index):
        if quest_index not in self.completed_quests:
            activity, stat = self.quests[quest_index]
            self.stats[stat] += 1
            self.completed_quests.append(quest_index)
            if len(self.completed_quests) == len(self.quests):
                self.stats['Discipline'] += 1
                self.stats['Willpower'] += 1
            self.update_level()
            return True
        return False

    def log_bad_habit(self):
        self.stats['Discipline'] -= 1
        self.stats['Willpower'] -= 1
        self.update_level()

    def calculate_punishment(self):
        incomplete_count = len(self.quests) - len(self.completed_quests)
        if incomplete_count > 0:
            return f"{incomplete_count} gut punch(es) from Jack."
        return "No punishment. All quests completed!"

def save_user_data(user):
    with open('user_data.pkl', 'wb') as f:
        pickle.dump(user, f)

def load_user_data():
    if os.path.exists('user_data.pkl'):
        with open('user_data.pkl', 'rb') as f:
            user = pickle.load(f)
            if user.last_login.date() < datetime.datetime.now().date():
                user.generate_quests()  # Generate new quests for a new day
            return user
    else:
        return User()

def display_quests(user):
    print("Today's Quests:")
    for i, (activity, stat) in enumerate(user.quests):
        completed = i in user.completed_quests
        display_text = f"{i+1}. {activity} to improve {stat}"
        if completed:
            display_text = strike(display_text)
        print(display_text)

def strike(text):
    return ''.join([u'\u0336{}'.format(c) for c in text])

def main():
    user = load_user_data()
    user.last_login = datetime.datetime.now()  # Update last login time
    if not user.quests:
        user.generate_quests()
    while True:
        print("\n1. Display Quests\n2. Complete Quest\n3. Log Bad Habit\n4. Show Stats\n5. Exit")
        choice = input("Choose an option: ")
        try:
            if choice == '1':
                display_quests(user)
            elif choice == '2':
                quest_index = int(input("Enter quest number to mark as complete: ")) - 1
                if quest_index >= len(user.quests) or quest_index < 0:
                    print("Invalid quest number, please try again.")
                elif not user.complete_quest(quest_index):
                    print("Quest already completed!")
                else:
                    print("Quest completed!")
            elif choice == '3':
                user.log_bad_habit()
                print("Bad habit logged!")
            elif choice == '4':
                print(f"Stats: {user.stats}")
                print(f"Level: {user.level}")
            elif choice == '5':
                punishment = user.calculate_punishment()
                print(f"Punishment for today: {punishment}")
                save_user_data(user)
                break
            else:
                print("Invalid option, please choose again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()
