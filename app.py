from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Game model with at least 4 fields
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(100))
    progress = db.Column(db.String(100))  # e.g., "Level 3" or "50% complete"
    completed = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer)  # 1-5 stars
    started_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f' <Game id={self.id} title={self.title} platform={self.platform} completed={self.completed}>'
    # asked professer the main reason for code, but based on resarch used during debugging and developing app

# Create the database and tables
with app.app_context():
    db.create_all()

# to display all games after users
@app.route('/')
def index():
    games = Game.query.order_by(Game.started_at.desc()).all()
    return render_template('index.html', games=games)

#  adding a new game entry
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    platform = request.form.get('platform')
    progress = request.form.get('progress')
    
    if title:  #  validation for title
        new_game = Game(
            title=title,
            platform=platform,
            progress=progress
        )
        db.session.add(new_game)
        db.session.commit()
    return redirect(url_for('index'))

#  game completion status and will appear on webpage as a completed click
@app.route('/toggle/<int:game_id>')
def toggle(game_id):
    game = Game.query.get_or_404(game_id)
    game.completed = not game.completed
    db.session.commit()
    return redirect(url_for('index'))


#  delete a game entry if user enters wrong thing or wants to delete it
@app.route('/delete/<int:game_id>')
def delete(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
