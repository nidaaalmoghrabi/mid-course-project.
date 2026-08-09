# Architecture: Task Tracker API

## 1. What it does

Task Tracker API is a small FastAPI learning project with a REST API and a vanilla JavaScript task-board frontend. It lets users create, list, read, update, and delete tasks; filter tasks by status, priority, or overdue state; and view a read-only activity log globally or for a single task.

The project is intentionally lightweight. It has no authentication, user accounts, database, background jobs, real-time updates, or cloud deployment. Task and activity state live in process memory and are lost when the server restarts. On local development startup, `app/main.py` seeds demo tasks unless `APP_ENV` is `test`, pytest is loaded, or the in-memory store already contains tasks.

## 2. Data model

The API contract is defined in `app/models.py`.

- `TaskStatus`: `ToDo`, `InProgress`, and `Done`.
- `TaskPriority`: `Low`, `Medium`, and `High`.
- `TaskCreate`: create payload with required `title`; default `description`, `status`, and `priority`; optional `assignee` and `due_date`.
- `TaskUpdate`: partial update payload for editable task fields.
- `TaskResponse`: stored task shape with UUID string `id`, task fields, `created_at`, and `updated_at`.
- `ActivityEntry`: read-only activity item with UUID string `id`, `task_id`, `task_title`, `action`, and `created_at`.
- `HealthResponse`: `/health` response with `status` and timestamp.

Create and update payloads reject unknown fields. Titles are stripped, cannot be blank, and cannot exceed 200 characters. `TaskUpdate.title` also rejects `null`. `due_date` is a date, not a datetime. Overdue state is calculated from `due_date < today` and `status != Done`; it is not stored as a field.

`app/storage.py` stores tasks in `_tasks: dict[str, TaskResponse]` and activity entries in `_activity: list[ActivityEntry]`. Task and activity IDs are UUID strings, and timestamps are timezone-aware UTC datetimes.

## 3. Request flow when a user creates a task

1. In `frontend/index.html`, the task form submit handler trims the title, builds a JSON payload, and sends `POST /tasks` with `Content-Type: application/json`.
2. In `app/main.py`, FastAPI routes the request to `create_task(payload: TaskCreate)`.
3. Pydantic validates the payload before route logic runs: required title, enum values, date parsing, title trimming, and forbidden extra fields.
4. The route handler calls `storage.add_task(payload)`.
5. `app/storage.py` generates a UUID task ID, captures the current UTC time, builds a `TaskResponse`, normalizes a missing description to an empty string, writes the task into `_tasks`, and records a `created task` activity entry in `_activity`.
6. FastAPI returns the created task with HTTP `201 Created`.
7. The frontend closes the modal, shows a success message, then refreshes the task board and activity panel from the API.

Status-transition validation in `app/business_rules.py` is not part of creation. It runs on updates when `PATCH /tasks/{task_id}` includes a new status.

## 4. Key files

- `app/__init__.py`: marks `app` as a Python package.
- `app/main.py`: creates the FastAPI app, configures CORS, seeds demo tasks, serves the frontend, and defines task and activity routes.
- `app/models.py`: owns Pydantic schemas, task enums, response shapes, and title validation.
- `app/storage.py`: owns in-memory task storage, filtering, lookup, updates, deletion, activity creation, activity listing, and test reset behavior.
- `app/business_rules.py`: defines allowed task status transitions and raises HTTP 422 for invalid transitions.
- `app/routes.py`: defines the `/health` router.
- `app/repository.py`: generic integer-keyed in-memory repository scaffold; not used by the current task storage path.
- `frontend/index.html`: browser board, modal form, filters, drag-and-drop updates, task cards, due and overdue indicators, and activity panel.
- `tests/conftest.py`: resets in-memory storage around tests.
- `tests/test_health.py`: covers the health endpoint.
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
- Use FastAPI response models and explicit status codes on routes.
- Record activity only for meaningful changes: creation, deletion, status transitions, and fields whose stored values actually changed.
- Do not record new activity when an update contains no changed values.
- Return activity most recent first, and keep the activity API read-only.
- Record delete activity before removing the task from `_tasks`.
- Calculate overdue state from the current UTC date at query/render time instead of storing it.
- Keep frontend API calls aligned with backend filters, especially `GET /tasks?overdue=true`.

## Context Strategy Comparison
### Strategy A - Minimal Context
What it got right: focused only on the immediate task surface and avoided unnecessary detail.
What it got wrong or invented: likely missed repo-wide conventions such as `extra="forbid"`, demo seeding behavior, and the unused `app/repository.py` scaffolding.

### Strategy B - Structured Context
What it got right: explains the repo’s full architecture, including API endpoints, frontend patterns, storage design, data models, validation rules, and test conventions.
What it got wrong or missed: may include more repository-level detail than required for a single small patch, but the extra context helps prevent incorrect assumptions.

### Strategy C - Targeted Context
What it got right: focuses only on the exact files and feature being changed, such as task/comment routes, Pydantic models, storage logic, and related tests.
What it got wrong or missed: may leave out broader constraints like the in-memory-only persistence policy, activity log semantics, demo data seeding behavior, and the fact that `app/repository.py` is unused.

### Verdict
I picked Strategy B because it gives a reliable architectural overview for this repo and reduces the risk of missing important cross-cutting conventions.

### My context rule
For architecture or design documentation, use Strategy B because it balances completeness, correctness, and clarity in a small codebase.
For a narrow feature implementation or bug fix, use Strategy C because it keeps the context focused on the files and behavior that matter most.
