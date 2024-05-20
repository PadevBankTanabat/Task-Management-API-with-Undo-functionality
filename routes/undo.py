# routes/undo.py
from flask import Blueprint, jsonify
from database import get_db_connection
from datetime import datetime

undo_bp = Blueprint('undo', __name__)

@undo_bp.route('/undo', methods=['POST'])
def undo_last_action():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM actions ORDER BY id DESC LIMIT 1')
    action = cursor.fetchone()

    if action is None:
        conn.close()
        return jsonify({'error': 'No actions to undo'}), 400

    action_type = action['action_type']
    task_id = action['task_id']
    task_data = eval(action['task_data'])  # Convert string back to dictionary

    if action_type == 'create':
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    elif action_type == 'update':
        cursor.execute('''
            UPDATE tasks
            SET title = ?, description = ?, due_date = ?, status = ?, updated_by = ?, updated_date = ?
            WHERE id = ?
        ''', (task_data['title'], task_data['description'], task_data['due_date'], task_data['status'], task_data['updated_by'], task_data['updated_date'], task_id))
    elif action_type == 'delete':
        cursor.execute('''
            INSERT INTO tasks (id, title, description, due_date, status, created_by, created_date, updated_by, updated_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (task_data['id'], task_data['title'], task_data['description'], task_data['due_date'], task_data['status'], task_data['created_by'], task_data['created_date'], task_data['updated_by'], task_data['updated_date']))

    conn.commit()
    cursor.execute('DELETE FROM actions WHERE id = ?', (action['id'],))
    conn.commit()
    conn.close()

    return jsonify({'result': 'Undo successful'}), 200

