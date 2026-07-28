# Task Tracker API

Task Tracker API is a small REST API learning project built with Python and FastAPI. It provides task CRUD endpoints, a simple browser-based task board, due dates with overdue filtering, and an in-memory activity log without authentication, database storage, Docker, or cloud deployment.

## Features

- Create, list, read, update, and delete tasks.
- Track task title, description, status, priority, assignee, and optional due date.
- Filter tasks by status, priority, or overdue state.
- Show due and overdue indicators on frontend task cards.
- Record simple activity events for task create, update, status change, and delete.
- View all activity or activity for a single task.

## Requirements

- Python 3.10 or newer
- `pip`

## Project Structure

```text
task-tracker-api/
|
|-- app/
|   |-- __init__.py
|   |-- business_rules.py
|   |-- main.py
|   |-- models.py
|   |-- repository.py
|   |-- routes.py
|   `-- storage.py
|
|-- frontend/
|   `-- index.html
|
|-- tests/
|   |-- __init__.py
|   |-- conftest.py
|   |-- test_health.py
|   `-- test_tasks.py
|
|-- .env.example
|-- README.md
`-- requirements.txt
```

## Create a Virtual Environment

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

After activation, the terminal normally displays the virtual environment name before the command prompt.

## Install Dependencies

Upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configure Environment Variables

Copy the example environment file.

### Linux/macOS

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item ".env.example" ".env"
```

The default configuration is:

```dotenv
PORT=8000
APP_ENV=development
```

## Start the Development Server

Run the following command from the project root:

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The API and task board frontend will be available at:

```text
http://127.0.0.1:8000
```

The automatic Swagger UI documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

The OpenAPI schema will be available at:

```text
http://127.0.0.1:8000/openapi.json
```

## Task API

Create a task:

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Write README\",\"assignee\":\"Alicia\",\"due_date\":\"2026-08-03\"}"
```

List tasks:

```bash
curl http://127.0.0.1:8000/tasks
```

Filter overdue tasks:

```bash
curl "http://127.0.0.1:8000/tasks?overdue=true"
```

Update a task:

```bash
curl -X PATCH http://127.0.0.1:8000/tasks/TASK_ID \
  -H "Content-Type: application/json" \
  -d "{\"assignee\":\"Marcus\"}"
```

Delete a task:

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/TASK_ID
```

## Activity API

The activity log records task create, update, status-change, and delete events.

View all activity:

```bash
curl http://127.0.0.1:8000/activity
```

View activity for one task:

```bash
curl http://127.0.0.1:8000/tasks/TASK_ID/activity
```

Activity update events only include fields that actually changed. For example, changing only the assignee records:

```text
updated assignee
```

Changing status records the previous and next status:

```text
changed status from ToDo to InProgress
```

Deleting a task records:

```text
deleted task
```

## Test the Health Endpoint with curl

Keep the Uvicorn server running and open another terminal.

Run:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "timestamp": "2026-07-20T19:30:15.245721Z"
}
```

The exact timestamp will be different for every request.

## Run the Automated Tests

From the project root, run:

```bash
python -m pytest
```

For more detailed output, run:

```bash
python -m pytest -v
```

## Stop the Server

Press:

```text
Ctrl+C
```

in the terminal where Uvicorn is running.
