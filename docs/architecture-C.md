# Architecture: Task Tracker API

## 1. What It does

This is a FastAPI task-tracking API with a small served frontend entry point. It exposes endpoints to list, create, retrieve, update, and delete tasks, plus endpoints to list activity globally or for a single task. Tasks can be filtered by status, priority, and overdue state. On local development startup, the app seeds demo tasks unless `APP_ENV` is `test`, pytest is loaded, or the in-memory store already contains tasks.

Behavior outside `app/main.py`, `app/models.py`, and `app/storage.py` is not visible from the files I read. The details of `app.business_rules.validate_status_transition` and `app.routes.router` are not visible from the files I read.

## 2. Data model

The API uses Pydantic models. `TaskCreate` accepts `title`, `description`, `status`, `priority`, `assignee`, and `due_date`. `TaskUpdate` accepts the same editable fields as optional partial-update values. `TaskResponse` adds server-generated `id`, `created_at`, and `updated_at`.

Task status is an enum with `ToDo`, `InProgress`, and `Done`. Task priority is an enum with `Low`, `Medium`, and `High`. Titles are stripped, must not be blank, and must not exceed 200 characters. Extra fields are forbidden on the visible models.

Activity is represented by `ActivityEntry`, with `id`, `task_id`, `task_title`, `action`, and `created_at`. A `HealthResponse` model exists with `status` and `timestamp`, but its use is not visible from the files I read.

## 3. Request flow when a user creates a task

A client sends `POST /tasks` with a JSON body matching `TaskCreate`. FastAPI validates and parses the request using the Pydantic model, including title normalization and enum/date validation. The `create_task` route in `app/main.py` passes the parsed payload to `storage.add_task`.

`storage.add_task` creates a UTC timestamp, generates a UUID string for the task id, builds a `TaskResponse`, stores it in the module-level `_tasks` dictionary, records a `"created task"` activity entry in `_activity`, and returns the new task. FastAPI serializes that `TaskResponse` back to the client with HTTP status `201 Created`.

Persistence beyond process memory is not visible from the files I read.

## 4. Key files

`app/main.py` creates the FastAPI app, configures CORS, seeds demo tasks, includes an external router, serves the frontend HTML file, and defines the visible task and activity endpoints.

`app/models.py` defines the visible Pydantic request/response models and task-related enums.

`app/storage.py` owns the in-memory task and activity stores, including create, list/filter, lookup, update, delete, activity retrieval, and test reset behavior.

## 5. Conventions

The visible storage layer is in-memory and module-scoped. Task and activity ids are UUID strings. Timestamps are generated with timezone-aware UTC datetimes. Public API models forbid extra fields. Create and update validation is handled by Pydantic models, while status-transition validation is invoked from `app/main.py`; the transition rules themselves are not visible from the files I read.

Task updates are partial and ignore unset fields. If an update contains no changed values, the existing task is returned without recording new activity. Activity entries are sorted newest first when listed. Deleted tasks record activity before being removed from `_tasks`.
