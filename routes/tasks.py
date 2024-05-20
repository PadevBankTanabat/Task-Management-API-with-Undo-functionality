# routes/tasks.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from database import get_db_connection
import sqlite3

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.json
        print('------------------------------ ', data)
        if not data:
            return jsonify({'error': 'Invalid input'}), 400
        
        title = data['title']
        description = data.get('description', '')
        due_date = data.get('due_date', None)
        status = data.get('status', 'pending')
        created_by = data['created_by']
        created_date = datetime.now().isoformat()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, description, due_date, status, created_by, created_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, description, due_date, status, created_by, created_date))
        conn.commit()
        task_id = cursor.lastrowid

        cursor.execute('''
            INSERT INTO actions (action_type, task_id, task_data, timestamp)
            VALUES (?, ?, ?, ?)
        ''', ('create', task_id, str(data), created_date))
        conn.commit()

        conn.close()
        return jsonify({'id': task_id, 'title': title, 'description': description, 'due_date': due_date, 'status': status, 'created_by': created_by, 'created_date': created_date}), 201

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error', 'message': str(e)}), 400
    except sqlite3.Error as e:
        return jsonify({'error': 'Database error', 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        due_date = request.args.get('due_date')
        status = request.args.get('status')
        created_by = request.args.get('created_by')
        updated_by = request.args.get('updated_by')

        query = 'SELECT * FROM tasks WHERE 1=1'
        params = []

        if due_date:
            query += ' AND due_date = ?'
            params.append(due_date)
        if status:
            query += ' AND status = ?'
            params.append(status)
        if created_by:
            query += ' AND created_by = ?'
            params.append(created_by)
        if updated_by:
            query += ' AND updated_by = ?'
            params.append(updated_by)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        tasks = cursor.fetchall()
        conn.close()

        return jsonify([dict(row) for row in tasks])

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error', 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
        conn.close()

        if task is None:
            return jsonify({'error': 'Task not found'}), 404

        return jsonify(dict(task))

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error', 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid input'}), 400
        
        title = data['title']
        description = data.get('description', '')
        due_date = data.get('due_date', None)
        status = data.get('status', 'pending')
        updated_by = data['updated_by']
        updated_date = datetime.now().isoformat()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()

        if task is None:
            conn.close()
            return jsonify({'error': 'Task not found'}), 404

        # Save current task data before updating
        current_task_data = {
            'title': task['title'],
            'description': task['description'],
            'due_date': task['due_date'],
            'status': task['status'],
            'updated_by': task['updated_by'],
            'updated_date': task['updated_date']
        }

        cursor.execute('''
            UPDATE tasks
            SET title = ?, description = ?, due_date = ?, status = ?, updated_by = ?, updated_date = ?
            WHERE id = ?
        ''', (title, description, due_date, status, updated_by, updated_date, task_id))
        conn.commit()

        # Store the current task data in the actions table
        cursor.execute('''
            INSERT INTO actions (action_type, task_id, task_data, timestamp)
            VALUES (?, ?, ?, ?)
        ''', ('update', task_id, str(current_task_data), updated_date))
        conn.commit()

        conn.close()
        return jsonify({'id': task_id, 'title': title, 'description': description, 'due_date': due_date, 'status': status, 'updated_by': updated_by, 'updated_date': updated_date})

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error', 'message': str(e)}), 400
    except sqlite3.Error as e:
        return jsonify({'error': 'Database error', 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()

        if task is None:
            conn.close()
            return jsonify({'error': 'Task not found'}), 404

        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()

        deleted_at = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO actions (action_type, task_id, task_data, timestamp)
            VALUES (?, ?, ?, ?)
        ''', ('delete', task_id, str(dict(task)), deleted_at))
        conn.commit()

        conn.close()
        return jsonify({'result': 'Task deleted'}), 200

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error', 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500
