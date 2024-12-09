from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import random
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulated database
users = {}

@app.route('/')
def index():
    # Assuming 'Player' is your default user for simplicity
    user = users.get('Player', User(name='Player'))
    users['Player'] = user
    return render_template('home.html', user=user)

@app.route('/complete_quest/<int:quest_index>', methods=['POST'])
def complete_quest(quest_index):
    user = users.get('Player')
    if user:
        success = user.complete_quest(quest_index)
        if success:
            flash('Quest completed!', 'success')
        else:
            flash('Quest already completed or invalid number!', 'error')
    return redirect(url_for('index'))


# Similar endpoints for logging habits, updating stats, etc.

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
        self.quests = self.generate_quests()
        self.completed_quests = []
        self.last_login = datetime.datetime.now()

    def generate_quests(self):
        activities = ['Gym', 'Study for 1 hour', 'Jog 21 mins', 'solve puzzles', 'meditate for 10 mins', 'plan your day']
        stats = ['Strength', 'Agility', 'Stamina', 'Intelligence', 'Willpower', 'Discipline']
        return random.sample(list(zip(activities, stats)), 4)

    def complete_quest(self, quest_index):
        if quest_index not in self.completed_quests:
            activity, stat = self.quests[quest_index]
            self.stats[stat] += 1
            self.completed_quests.append(quest_index)
            if len(self.completed_quests) == len(self.quests):
                self.stats['Discipline'] += 1
                self.stats['Willpower'] += 1
            return True
        return False

if __name__ == '__main__':
    app.run(debug=True)
