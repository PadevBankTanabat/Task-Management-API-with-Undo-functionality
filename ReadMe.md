# Task Management API

![Task Management API](https://img.shields.io/badge/Task%20Management-API-blue.svg)

This is a Task Management API built with Flask and SQLite. It allows users to create, update, delete, and view tasks. Additionally, it supports an "undo" functionality, enabling users to reverse their last action.

## Project Structure

The project has the following structure:

Task-Management-API-with-Undo-functionality/

├── app.py

├── database.py

└── routes/

        ├── tasks.py

        └── undo.py

## Setup

1. Ensure you have Python 3.6+ installed.

2. Install the required packages:

```bash

pip install flask sqlite3

```

3. Run the application:

```bash

python app.py

```

The application will be accessible at [http://localhost:5000](http://localhost:5000).

## Testing

You can test the application using any API testing tool like Postman or curl. Here are some examples of how to test the different endpoints:

#### Create a Task

```
curl  -X  POST  -H  "Content-Type: application/json"  -d  '
   {
    "title":"title",
    "description":"Lorem Ipsum is simply dummy text...",
    "due_date":"2024-01-01",
    "status":"pending",
    "created_by":"Strike Social"
    }'   
    
    http://localhost:5000/tasks

```

#### Get All Tasks

```
curl -X GET http://localhost:5000/tasks
```

#### Get a Specific Task

Replace  `<task_id>`  with the ID of the task you want to retrieve.

```
`curl -X GET http://localhost:5000/tasks/<task_id>`
```

#### Update a Task

Replace  `<task_id>`  with the ID of the task you want to update.

```
`curl -X PUT -H "Content-Type: application/json" -d '

{
    "description": "Lorem Ipsum is simply dummy text...",
    "due_date": "2024-01-01",
    "status": "pending",
    "title": "updated title",
    "updated_by": user,
    "updated_date": null
}

' http://localhost:5000/tasks/<task_id>`
```

#### Delete a Task

Replace  `<task_id>`  with the ID of the task you want to delete.

```
`curl -X DELETE http://localhost:5000/tasks/<task_id>`
```

#### Undo the Last Action

```
`curl -X POST http://localhost:5000/undo`
```

## Viewing the Database Structure and Data

#### 1. Open the SQLite database

```
sqlite3 tasksManagement.db
```

#### 2. List all tables

This command will show you all the tables present in the tasksManagemt.db database.

```
.tables
```

#### 3. View the schema of a specific table

Replace '<table_name>' with the name of the table you want to inspect.
This command provides the structure of the specified table, showing the columns and their data types.

```
.schema <table_name>
```

#### 4. Display all data from a table

Replace <table_name> with the name of the table from which you want to fetch the data.
This will display all rows and columns from the specified table.

```
SELECT * FROM <table_name>;
```

### Example Session

```
sqlite3 tasksManagement.db
SQLite version 3.32.3 2024-05-20 12:34:56
Enter ".help" for usage hints.
sqlite> .tables
actions  tasks
sqlite> .schema tasks
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    due_date DATE,
    status TEXT,
    created_by TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by TEXT,
    updated_date DATETIME
);
sqlite> SELECT * FROM tasks;
1|Task 1|Description for Task 1|2024-01-01|pending|User A|2024-01-01 10:00:00|User B|2024-01-02 11:00:00
2|Task 2|Description for Task 2|2024-02-01|completed|User C|2024-02-01 12:00:00|User D|2024-02-02 13:00:00
sqlite> .schema actions
CREATE TABLE actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_type TEXT NOT NULL,
    task_id INTEGER,
    action_data TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
sqlite> SELECT * FROM actions;
1|create|1|{"title": "Task 1", "description": "Description for Task 1", ...}|2024-01-01 10:00:00
2|update|1|{"status": "completed"}|2024-01-02 11:00:00
3|delete|2|{}|2024-02-02 13:30:00

```

## Requirements

This API is designed to meet the following requirements:

- **CRUD Operations**: The API allows users to perform basic CRUD (Create, Read, Update, Delete) operations on tasks. Each task has a title, description, due date, status (e.g., "pending", "in progress", "completed"), and information about the user who created and last updated the task. Users can retrieve tasks that match specific due dates, statuses, or created/updated users.
- **Undo Functionality**: The API supports the "undo" functionality, which enables users to revert their last action. For instance, if a user accidentally deleted a task, they can undo the deletion and recover the task.

## Considerations

- **Data Storage**: The API uses SQLite for data storage.
- **Programming Language and Frameworks**: The API is implemented in Python using the Flask framework.
- **Error Handling**: The API implements proper error handling to ensure it behaves gracefully and provides informative error messages to users.
- **Undo Mechanism**: The API keeps track of user actions in a separate actions table in the database, enabling users to undo previous operations.
- **Code Quality**: The code is clean, modular, and well-documented. Comments are used to explain design choices and any trade-offs made during implementation.
