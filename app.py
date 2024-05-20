# app.py
from flask import Flask
from database import init_db
from routes.tasks import tasks_bp
from routes.undo import undo_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(tasks_bp)
app.register_blueprint(undo_bp)

# Initialize the database
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)
