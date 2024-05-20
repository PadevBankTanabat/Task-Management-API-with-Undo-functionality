import sqlite3

def get_db_connection():
    conn = sqlite3.connect('tasksManagement.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT CHECK(status IN ('pending', 'in progress', 'completed')),
            created_by TEXT NOT NULL,
            updated_by TEXT,
            created_date TEXT,
            updated_date TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type TEXT NOT NULL,
            task_id INTEGER,
            task_data TEXT,
            timestamp TEXT
    )
    ''')
    conn.commit()
    conn.close()
