"""Create and configure the FastAPI application."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app import storage
from app.business_rules import validate_status_transition
from app.models import ActivityEntry, TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate
from app.routes import router


# Load environment variables from the .env file.
load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")

# Create the FastAPI application.
app = FastAPI(
    title="Task Tracker API",
    description="A simple Task Tracker REST API learning project.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)


def seed_demo_tasks() -> None:
    if os.getenv("APP_ENV") == "test" or "pytest" in sys.modules:
        return

    if storage.get_all_tasks():
        return

    demo_tasks = [
        TaskCreate(
            title="Draft release notes",
            description="Summarize the key updates for the upcoming release.",
            status=TaskStatus.TODO,
            priority=TaskPriority.HIGH,
            assignee="Alicia",
            due_date="2026-07-24",
        ),
        TaskCreate(
            title="Implement onboarding flow",
            description="Add the first-run experience and welcome checklist.",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.MEDIUM,
            assignee="Marcus",
            due_date="2026-07-30",
        ),
        TaskCreate(
            title="Ship bugfixes",
            description="Close the top customer-reported issues from last week.",
            status=TaskStatus.DONE,
            priority=TaskPriority.LOW,
            assignee="Unassigned",
        ),
    ]

    for task in demo_tasks:
        storage.add_task(task)


seed_demo_tasks()

# Add the routes to the application.
app.include_router(router)


@app.get("/", tags=["frontend"])
def serve_frontend() -> FileResponse:
    frontend_path = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
    return FileResponse(frontend_path)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    overdue: bool | None = None,
) -> list[TaskResponse]:
    return storage.get_all_tasks(status=status, priority=priority, overdue=overdue)


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    return storage.add_task(payload)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.get("/activity", response_model=list[ActivityEntry], tags=["activity"])
def list_activity() -> list[ActivityEntry]:
    return storage.get_activity()


@app.get("/tasks/{task_id}/activity", response_model=list[ActivityEntry], tags=["activity"])
def list_task_activity(task_id: str) -> list[ActivityEntry]:
    return storage.get_activity(task_id=task_id)


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        validate_status_transition(existing.status, payload.status)

    task = storage.update_task(task_id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    if not storage.delete_task(task_id):
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
