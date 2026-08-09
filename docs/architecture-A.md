# Architecture A

## 1. What it does

Task Tracker is a small FastAPI application for managing tasks through both a REST API and a single-page browser board. Repository evidence in `README.md`, `app/main.py`, and `frontend/index.html` shows support for creating, listing, reading, updating, and deleting tasks; filtering by status, priority, or overdue state; and viewing task activity. The project is intentionally lightweight: the README states there is no authentication, database storage, or cloud deployment, and `app/storage.py` keeps state in memory.

## 2. Data model

The API schemas live in `app/models.py`.

- `TaskStatus`: `ToDo`, `InProgress`, `Done`.
- `TaskPriority`: `Low`, `Medium`, `High`.
- `TaskCreate`: create payload with required `title`; optional/defaulted `description`, `status`, `priority`, `assignee`, and `due_date`.
- `TaskUpdate`: partial update payload for the same editable task fields.
- `TaskResponse`: stored task shape with `id`, task fields, `created_at`, and `updated_at`.
- `ActivityEntry`: activity log item with `id`, `task_id`, `task_title`, `action`, and `created_at`.
- `HealthResponse`: `/health` response with `status` and `timestamp`.

`TaskCreate` and `TaskUpdate` forbid unknown fields through Pydantic config. Titles are stripped and must be non-blank and at most 200 characters. `app/storage.py` stores tasks in a module-level `_tasks: dict[str, TaskResponse]` and activity entries in `_activity: list[ActivityEntry]`; IDs are UUID strings and timestamps are timezone-aware UTC datetimes.

## 3. Request flow when a user creates a task

1. In `frontend/index.html`, the task form submit handler trims the title, builds a JSON payload, and sends `POST /tasks` with `Content-Type: application/json`.
2. In `app/main.py`, `create_task(payload: TaskCreate)` receives the request. FastAPI/Pydantic validates required fields, enum values, date parsing, title rules, and forbidden extra fields before the handler runs.
3. The route handler calls `storage.add_task(payload)`.
4. `app/storage.py` creates a UUID task id, captures the current UTC time, builds a `TaskResponse`, normalizes a missing description to an empty string, and writes the task to `_tasks`.
5. `storage.add_task` calls `_add_activity(task, "created task")`, which appends an `ActivityEntry` to `_activity`.
6. FastAPI returns the `TaskResponse` with HTTP `201 Created`. The frontend closes the modal, shows a success message, then refreshes tasks and activity with `fetchTasks()` and `fetchActivity()`.

Status-transition validation in `app/business_rules.py` is used for updates, not task creation; create requests may choose any valid `TaskStatus` enum value.

## 4. Key files

- `app/main.py`: FastAPI app construction, CORS, demo seeding, frontend serving, task routes, and activity routes.
- `app/models.py`: Pydantic models, enums, and task title validation.
- `app/storage.py`: in-memory task persistence, filtering, updates, deletes, and activity recording.
- `app/business_rules.py`: allowed status transitions for task updates.
- `app/routes.py`: `/health` router.
- `frontend/index.html`: task board UI and browser-side API calls.
- `tests/test_tasks.py`: endpoint and behavior coverage for CRUD, filters, transitions, and activity.
- `tests/conftest.py`: test client fixture and storage reset around each test.
- `README.md`: documented project scope, setup, module responsibilities, and conventions.

## 5. Conventions

- Keep public functions and route handlers documented with Google-style docstrings, as described in `README.md`.
- Keep request/response contracts in `app/models.py`; use Pydantic validation instead of route-local parsing.
- Keep business rules that are not pure schema validation in focused modules such as `app/business_rules.py`.
- Treat `app/storage.py` as volatile in-memory persistence. Tests reset it through `storage._reset()` in `tests/conftest.py`.
- Use FastAPI response models and explicit status codes on routes.
- Preserve the existing enum string values because the frontend and tests send and assert those exact values.
