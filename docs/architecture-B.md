# Architecture B

## 1. What it does

Task Tracker is a small FastAPI learning project with a REST API and a vanilla JavaScript task-board frontend. It lets users create, list, read, update, and delete tasks; filter tasks by status, priority, or overdue state; and view a read-only activity log. It intentionally has no authentication, user accounts, database, background jobs, real-time updates, or cloud deployment. Task and activity state live in process memory and are lost when the server restarts.

## 2. Data model

The API contract is defined in `app/models.py`.

- `TaskStatus`: `ToDo`, `InProgress`, and `Done`.
- `TaskPriority`: `Low`, `Medium`, and `High`.
- `TaskCreate`: create payload with required `title`; default `description`, `status`, and `priority`; optional `assignee` and `due_date`.
- `TaskUpdate`: partial update payload for editable task fields.
- `TaskResponse`: stored task shape with UUID string `id`, task fields, `created_at`, and `updated_at`.
- `ActivityEntry`: read-only activity item with UUID string `id`, `task_id`, `task_title`, `action`, and `created_at`.
- `HealthResponse`: `/health` response with `status` and timestamp.

Create and update payloads reject unknown fields. Titles are stripped, cannot be blank, and cannot exceed 200 characters. `due_date` is a date, not a datetime. Overdue is calculated from `due_date < today` and `status != Done`; it is not stored as a field. `app/storage.py` stores tasks in `_tasks: dict[str, TaskResponse]` and activity entries in `_activity: list[ActivityEntry]`.

## 3. Request flow when a user creates a task

1. The browser form in `frontend/index.html` builds a JSON payload and sends `POST /tasks` to the API.
2. FastAPI routes the request to `create_task(payload: TaskCreate)` in `app/main.py`.
3. Pydantic validates the payload before route logic runs: required title, enum values, date parsing, title trimming, and forbidden extra fields.
4. The route calls `storage.add_task(payload)`.
5. `app/storage.py` generates a UUID task id, captures the current UTC time, builds a `TaskResponse`, writes it into `_tasks`, and records a `created task` activity entry in `_activity`.
6. FastAPI returns the created task with HTTP `201 Created`.
7. The frontend refreshes the board and activity panel from the API.

Status-transition validation in `app/business_rules.py` is not part of creation. It runs on updates when `PATCH /tasks/{task_id}` includes a new status.

## 4. Key files

- `app/__init__.py`: marks `app` as a Python package.
- `app/main.py`: creates the FastAPI app, configures CORS, seeds demo tasks, serves the frontend, and defines task/activity routes.
- `app/models.py`: owns Pydantic schemas, task enums, response shapes, and title validation.
- `app/storage.py`: owns in-memory task storage, filtering, updates, deletion, activity creation, activity listing, and test reset behavior.
- `app/business_rules.py`: defines allowed task status transitions and raises HTTP 422 for invalid transitions.
- `app/routes.py`: defines the `/health` router.
- `app/repository.py`: generic integer-keyed in-memory repository scaffold; not used by the current task storage path.
- `frontend/index.html`: browser board, modal form, filters, drag-and-drop updates, task cards, and activity panel.
- `tests/conftest.py`: resets in-memory storage around tests.
- `tests/test_tasks.py`: covers task CRUD, validation, filters, status transitions, due dates, and activity behavior.
- `README.md`: documents setup, supported commands, scope, business rules, and module responsibilities.
- `docs/midcourse/*`: records feature decisions, verification evidence, prompt history, and storage trade-offs.

## 5. Conventions

- Keep the project small: no database, authentication, background jobs, notifications, real-time updates, or new frontend framework without explicit approval.
- Keep public route handlers and public functions documented with Google-style docstrings.
- Keep request and response validation in `app/models.py` using Pydantic v2.
- Keep cross-field or workflow rules, such as status transitions, outside the schemas in focused modules.
- Preserve exact status and priority string values because the API, frontend, and tests rely on them.
- Treat `app/storage.py` data as volatile process-local state. Use `_reset()` only for tests.
- Record activity only for meaningful changes: creation, deletion, status transitions, and fields whose stored values actually changed.
- Return activity most recent first, and keep the activity API read-only.
- Calculate overdue state from the current UTC date at query/render time instead of storing it.
- Keep frontend API calls aligned with backend filters, especially `GET /tasks?overdue=true`.
