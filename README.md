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
|-- .github/
|   `-- workflows/ci.yml
|-- .dockerignore
|-- .env.example
|-- Dockerfile
|-- AGENTS.md
|-- CLAUDE.md
|-- README.md
|-- requirements.txt
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
|-- docs/
|   |-- ai-playbook.md
|   |-- ai-usage.md
|   |-- architecture.md
|   `-- release-evidence.md
|
|-- tests/
|   |-- __init__.py
|   |-- conftest.py
|   |-- test_health.py
|   `-- test_tasks.py
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

## Final Project

Branch reviewed: final-project

### What this submission demonstrates
- Existing Task Tracker app still runs inside the intended course scope.
- CI runs the pytest suite on push and/or pull request.
- Docker image builds and runs with /health returning 200.
- AI review, security, and ownership evidence is in docs/.

### How to run locally
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### How to run tests
```powershell
python -m pytest
```

### How to run with Docker
```powershell
docker build -t task-tracker-api .
docker run --rm -p 8000:8000 task-tracker-api
```

In another terminal:

```powershell
curl http://127.0.0.1:8000/health
```

### Evidence files
- docs/release-evidence.md
- docs/final-ai-review.md
- docs/ai-playbook.md

### AI assistance summary
AI helped draft or review: CI workflow, Dockerfile, documentation, security review, debugging (an ESLint failure, a Docker Desktop engine issue, a datetime deprecation warning).
I verified the work by: running the pytest suite directly, building and running the actual Docker image and confirming `/health` returned 200 (both via the container's access log and an external `curl`), running `npm run lint` / `npm run build` locally, and sending real requests through Thunder Client.
One AI suggestion I rejected or corrected: a suggestion to rename `backend/` to `app/` to match the rubric's literal folder naming — rejected as an unnecessarily broad, cross-cutting change; documented the equivalence instead in `docs/repo-structure-mapping.md`.

