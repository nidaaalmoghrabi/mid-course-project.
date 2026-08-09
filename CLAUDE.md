# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Task Tracker API — a small FastAPI learning project providing task CRUD, due-date/overdue filtering, and an in-memory activity log. No auth, no database, no Docker/cloud deployment. State lives entirely in process memory and resets on restart.

## Commands

Activate the venv first (Windows PowerShell): `.\.venv\Scripts\Activate.ps1`

Run the dev server (serves both the API and the frontend at the same origin):
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Run all tests:
```bash
python -m pytest
```

Run a single test file or test:
```bash
python -m pytest tests/test_tasks.py
python -m pytest tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422 -v
```

`.env` is loaded via `python-dotenv`; relevant vars are `PORT` and `APP_ENV` (set `APP_ENV=test` to skip demo data seeding — pytest runs also auto-skip seeding because `conftest.py` triggers `pytest` module detection).

## Architecture

- **`app/main.py`** — creates the `FastAPI` app, configures CORS, seeds demo tasks on startup (skipped under `APP_ENV=test` or when running under pytest), serves `frontend/index.html` at `/`, and defines the task and activity endpoints (`/tasks`, `/tasks/{id}`, `/activity`, `/tasks/{id}/activity`) directly on `app`. Only `/health` lives on the separate router in `app/routes.py` — new endpoints should generally follow the existing pattern of being added directly to `main.py` alongside the task/activity routes rather than the router, unless you're intentionally restructuring.
- **`app/storage.py`** — the actual persistence layer: two module-level dicts/lists (`_tasks`, `_activity`) manipulated directly (no DB, no ORM). Every task mutation (`add_task`, `update_task`, `delete_task`) also appends a human-readable entry to the activity log via `_add_activity`. `update_task` diffs the incoming `TaskUpdate` against the existing task, only applies fields that actually changed, and builds the activity message from that diff (e.g. `"changed status from ToDo to InProgress"`, `"updated assignee, priority"`) — when adding new updatable fields, extend `_ACTIVITY_FIELD_LABELS` so the activity text stays readable. `_reset()` clears all state and is called by the test fixtures between tests.
- **`app/models.py`** — all Pydantic models (`TaskCreate`, `TaskUpdate`, `TaskResponse`, `ActivityEntry`, `HealthResponse`) and the `TaskStatus`/`TaskPriority` enums. All models use `extra="forbid"`, so unknown request fields are rejected with 422. Title validation (non-blank, ≤200 chars) is shared between create/update via the `_validate_title` helper.
- **`app/business_rules.py`** — status-transition validation (`validate_status_transition`), enforced only on `PATCH /tasks/{id}` when a `status` change is requested. Valid transitions are an explicit allowlist in `VALID_TRANSITIONS` (ToDo→InProgress, InProgress→Done, Done→InProgress); anything else, including a no-op same-status "change", is rejected with 422.
- **`app/repository.py`** — a generic `InMemoryRepository` scaffold that is not currently wired into `storage.py` or anything else; `storage.py` implements persistence independently with its own module-level dict. Be aware of this when working on storage-related changes — it's dead/unused scaffolding, not the active storage mechanism.
- **`frontend/index.html`** — single self-contained static HTML/JS/CSS file (no build step, no framework) that renders the task board and calls the API. Served by the `/` route in `main.py`.

## Testing

- `tests/conftest.py` provides `client` (a `TestClient`) and `created_task` fixtures, and an autouse fixture that calls `storage._reset()` before and after every test so tests don't leak state.
- Tests hit the API through `TestClient`, not the storage layer directly — follow this convention for new tests.
