"""In-memory storage for tasks."""

import uuid
from datetime import datetime, timezone
from typing import Optional

from app.models import ActivityEntry, TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

_tasks: dict[str, TaskResponse] = {}
_activity: list[ActivityEntry] = []
_ACTIVITY_FIELD_LABELS = {
    "assignee": "assignee",
    "description": "description",
    "due_date": "due date",
    "priority": "priority",
    "title": "title",
}


def _add_activity(task: TaskResponse, action: str) -> ActivityEntry:
    entry = ActivityEntry(
        id=str(uuid.uuid4()),
        task_id=task.id,
        task_title=task.title,
        action=action,
        created_at=datetime.now(timezone.utc),
    )
    _activity.append(entry)
    return entry


def add_task(payload: TaskCreate) -> TaskResponse:
    now = datetime.now(timezone.utc)
    task_id = str(uuid.uuid4())
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    _add_activity(task, "created task")
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    overdue: Optional[bool] = None,
) -> list[TaskResponse]:
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    if overdue is not None:
        today = datetime.now(timezone.utc).date()
        tasks = [
            task
            for task in tasks
            if bool(task.due_date is not None and task.due_date < today and task.status != TaskStatus.DONE)
            == overdue
        ]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    task = _tasks.get(task_id)
    if task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return task

    changed_updates = {
        field: value
        for field, value in updates.items()
        if getattr(task, field) != value
    }
    if not changed_updates:
        return task

    updated_task = task.model_copy(update={**changed_updates, "updated_at": datetime.now(timezone.utc)})
    _tasks[task_id] = updated_task

    actions: list[str] = []
    if "status" in changed_updates:
        actions.append(f"changed status from {task.status.value} to {updated_task.status.value}")

    changed_fields = sorted(
        _ACTIVITY_FIELD_LABELS.get(field, field)
        for field in changed_updates
        if field != "status"
    )
    if changed_fields:
        actions.append(f"updated {', '.join(changed_fields)}")

    _add_activity(updated_task, "; ".join(actions))
    return updated_task


def delete_task(task_id: str) -> bool:
    if task_id not in _tasks:
        return False
    _add_activity(_tasks[task_id], "deleted task")
    del _tasks[task_id]
    return True


def get_activity(task_id: Optional[str] = None) -> list[ActivityEntry]:
    entries = _activity
    if task_id is not None:
        entries = [entry for entry in entries if entry.task_id == task_id]
    return sorted(entries, key=lambda entry: entry.created_at, reverse=True)


def _reset() -> None:
    _tasks.clear()
    _activity.clear()
