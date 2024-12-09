import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, font
import random
import pickle
import os
import datetime

class User:
    def __init__(self, name="Player"):
        self.name = name
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
        self.generate_quests()

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

def load_user_data():
    if os.path.exists('user_data.pkl'):
        with open('user_data.pkl', 'rb') as f:
            user = pickle.load(f)
            if user.last_login.date() < datetime.datetime.now().date():
                user.generate_quests()
            return user
    else:
        name = simpledialog.askstring("Name", "Enter your name:")
        return User(name=name)

def save_user_data(user):
    with open('user_data.pkl', 'wb') as f:
        pickle.dump(user, f)

class Application(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.title("The System")
        self.configure(bg='#0f0f0f')
        self.geometry("500x400")  # Slightly larger for aesthetic purposes
        self.custom_font = font.Font(family="Helvetica", size=12, weight="bold")  # Initialize the font here
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Welcome, {self.user.name}!", font=self.custom_font, fg="#00ff00", bg="#0f0f0f").pack(pady=10)
        tk.Label(self, text=f"Level: {self.user.level}", font=self.custom_font, fg="#00ff00", bg="#0f0f0f").pack(pady=5)
        
        stats_info = '\n'.join([f"{key}: {value}" for key, value in self.user.stats.items()])
        self.stats_label = tk.Label(self, text=stats_info, font=self.custom_font, fg="#00ff00", bg="#0f0f0f")
        self.stats_label.pack(pady=10)

        tk.Button(self, text="Show Quests", command=self.show_quests, font=self.custom_font, fg="#ffffff", bg="#333333").pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Complete Quest", command=self.complete_quest, font=self.custom_font, fg="#ffffff", bg="#333333").pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Log Bad Habit", command=self.log_bad_habit, font=self.custom_font, fg="#ffffff", bg="#333333").pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Exit", command=self.exit_app, font=self.custom_font, fg="#ffffff", bg="#333333").pack(fill=tk.X, padx=50, pady=5)

    def show_quests(self):
        quest_window = Toplevel(self)
        quest_window.title("Quests")
        quest_window.configure(bg='#0f0f0f')
        for i, (activity, stat) in enumerate(self.user.quests):
            completed = i in self.user.completed_quests
            text = f"{activity} to improve {stat}"
            label = tk.Label(quest_window, text=text, font=self.custom_font, fg="#00ff00" if completed else "#ffffff", bg="#0f0f0f")
            label.pack(pady=2)

    def complete_quest(self):
        quest_index = simpledialog.askinteger("Input", "Enter quest number to complete:")
        if quest_index and 0 <= quest_index - 1 < len(self.user.quests):
            success = self.user.complete_quest(quest_index - 1)
            message = "Quest completed!" if success else "Quest already completed or invalid number!"
            messagebox.showinfo("Info", message)
            self.update_stats_label()

    def log_bad_habit(self):
        self.user.log_bad_habit()
        messagebox.showinfo("Info", "Bad habit logged!")
        self.update_stats_label()

    def update_stats_label(self):
        stats_info = '\n'.join([f"{key}: {value}" for key, value in self.user.stats.items()])
        self.stats_label.config(text=stats_info)

    def exit_app(self):
        punishment = self.user.calculate_punishment()
        messagebox.showinfo("Punishment", punishment)
        save_user_data(self.user)
        self.destroy()

if __name__ == "__main__":
    user = load_user_data()
    app = Application(user)
    app.mainloop()
