from fastapi.testclient import TestClient


def test_create_task_valid_returns_201_with_full_body(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Write tests",
            "description": "Cover task endpoints",
            "status": "ToDo",
            "priority": "High",
            "assignee": "alice",
            "due_date": "2026-08-03",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert set(body) == {
        "id",
        "title",
        "description",
        "status",
        "priority",
        "assignee",
        "due_date",
        "created_at",
        "updated_at",
    }
    assert body["title"] == "Write tests"
    assert body["description"] == "Cover task endpoints"
    assert body["status"] == "ToDo"
    assert body["priority"] == "High"
    assert body["assignee"] == "alice"
    assert body["due_date"] == "2026-08-03"
    assert body["created_at"]
    assert body["updated_at"]


def test_create_task_missing_title_returns_422(client: TestClient) -> None:
    response = client.post("/tasks", json={"description": "no title"})

    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "Valid title", "priority": "Urgent"})

    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "Valid title", "made_up": "value"})

    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client: TestClient) -> None:
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(
    client: TestClient,
) -> None:
    client.post("/tasks", json={"title": "Open task", "status": "ToDo"})

    response = client.get("/tasks", params={"status": "Done"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client: TestClient) -> None:
    client.post("/tasks", json={"title": "Low task", "priority": "Low"})
    client.post("/tasks", json={"title": "High task", "priority": "High"})
    client.post("/tasks", json={"title": "Another high task", "priority": "High"})

    response = client.get("/tasks", params={"priority": "High"})

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert all(task["priority"] == "High" for task in tasks)


def test_list_tasks_filter_by_overdue_returns_only_open_overdue_tasks(
    client: TestClient,
) -> None:
    client.post("/tasks", json={"title": "Overdue task", "due_date": "2026-01-01"})
    client.post("/tasks", json={"title": "Future task", "due_date": "2999-01-01"})
    client.post("/tasks", json={"title": "No due date"})
    client.post(
        "/tasks",
        json={"title": "Done overdue task", "status": "Done", "due_date": "2026-01-01"},
    )

    response = client.get("/tasks", params={"overdue": "true"})

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Overdue task"


def test_get_task_by_id_returns_task(client: TestClient, created_task: dict) -> None:
    response = client.get(f"/tasks/{created_task['id']}")

    assert response.status_code == 200
    assert response.json() == created_task


def test_get_task_by_id_not_found_returns_404_with_detail(client: TestClient) -> None:
    missing_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/tasks/{missing_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Task with id {missing_id} not found"}


def test_patch_partial_update_keeps_other_fields(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"title": "updated title"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "updated title"
    assert body["description"] == created_task["description"]
    assert body["status"] == created_task["status"]
    assert body["priority"] == created_task["priority"]
    assert body["assignee"] == created_task["assignee"]
    assert body["due_date"] == created_task["due_date"]
    assert body["id"] == created_task["id"]
    assert body["created_at"] == created_task["created_at"]


def test_patch_due_date_updates_task(client: TestClient, created_task: dict) -> None:
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"due_date": "2026-08-04"},
    )

    assert response.status_code == 200
    assert response.json()["due_date"] == "2026-08-04"


def test_patch_not_found_returns_404(client: TestClient) -> None:
    missing_id = "00000000-0000-0000-0000-000000000000"
    response = client.patch(f"/tasks/{missing_id}", json={"title": "nope"})

    assert response.status_code == 404
    assert response.json() == {"detail": f"Task with id {missing_id} not found"}


def test_patch_valid_transition_todo_to_inprogress_returns_200(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "Done"},
    )

    assert response.status_code == 422
    assert "Invalid status transition from ToDo to Done" in response.json()["detail"]


def test_patch_invalid_transition_inprogress_back_to_todo_returns_422(
    client: TestClient,
) -> None:
    create_response = client.post(
        "/tasks",
        json={"title": "In progress task", "status": "InProgress"},
    )
    assert create_response.status_code == 201
    task = create_response.json()

    response = client.patch(
        f"/tasks/{task['id']}",
        json={"status": "ToDo"},
    )

    assert response.status_code == 422
    assert "Invalid status transition from InProgress to ToDo" in response.json()["detail"]


def test_patch_same_status_returns_422(client: TestClient, created_task: dict) -> None:
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "ToDo"},
    )

    assert response.status_code == 422
    assert "Invalid status transition from ToDo to ToDo" in response.json()["detail"]


def test_delete_existing_returns_204_no_body(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.delete(f"/tasks/{created_task['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client: TestClient) -> None:
    missing_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/tasks/{missing_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Task with id {missing_id} not found"}


def test_activity_records_create_event(client: TestClient) -> None:
    create_response = client.post("/tasks", json={"title": "Create activity"})
    assert create_response.status_code == 201
    task = create_response.json()

    response = client.get(f"/tasks/{task['id']}/activity")

    assert response.status_code == 200
    entries = response.json()
    assert len(entries) == 1
    assert entries[0]["task_id"] == task["id"]
    assert entries[0]["task_title"] == "Create activity"
    assert entries[0]["action"] == "created task"


def test_activity_lists_create_and_update_entries(
    client: TestClient,
    created_task: dict,
) -> None:
    patch_response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"priority": "High"},
    )
    assert patch_response.status_code == 200

    response = client.get("/activity")

    assert response.status_code == 200
    entries = response.json()
    assert len(entries) == 2
    assert entries[0]["task_id"] == created_task["id"]
    assert entries[0]["action"] == "updated priority"
    assert entries[1]["action"] == "created task"


def test_activity_records_only_fields_that_changed(
    client: TestClient,
    created_task: dict,
) -> None:
    patch_response = client.patch(
        f"/tasks/{created_task['id']}",
        json={
            "title": created_task["title"],
            "description": created_task["description"],
            "priority": created_task["priority"],
            "assignee": "bob",
            "due_date": created_task["due_date"],
        },
    )
    assert patch_response.status_code == 200

    response = client.get(f"/tasks/{created_task['id']}/activity")

    assert response.status_code == 200
    entries = response.json()
    assert entries[0]["action"] == "updated assignee"


def test_activity_uses_readable_field_names(
    client: TestClient,
    created_task: dict,
) -> None:
    patch_response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"due_date": "2026-08-04"},
    )
    assert patch_response.status_code == 200

    response = client.get(f"/tasks/{created_task['id']}/activity")

    assert response.status_code == 200
    entries = response.json()
    assert entries[0]["action"] == "updated due date"


def test_activity_does_not_record_when_values_do_not_change(
    client: TestClient,
    created_task: dict,
) -> None:
    patch_response = client.patch(
        f"/tasks/{created_task['id']}",
        json={
            "title": created_task["title"],
            "description": created_task["description"],
            "priority": created_task["priority"],
            "assignee": created_task["assignee"],
            "due_date": created_task["due_date"],
        },
    )
    assert patch_response.status_code == 200

    response = client.get(f"/tasks/{created_task['id']}/activity")

    assert response.status_code == 200
    entries = response.json()
    assert len(entries) == 1
    assert entries[0]["action"] == "created task"


def test_activity_records_status_change_event(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )
    assert response.status_code == 200

    activity_response = client.get(f"/tasks/{created_task['id']}/activity")

    assert activity_response.status_code == 200
    entries = activity_response.json()
    assert entries[0]["action"] == "changed status from ToDo to InProgress"


def test_activity_records_delete_event(client: TestClient, created_task: dict) -> None:
    delete_response = client.delete(f"/tasks/{created_task['id']}")
    assert delete_response.status_code == 204

    activity_response = client.get(f"/tasks/{created_task['id']}/activity")

    assert activity_response.status_code == 200
    entries = activity_response.json()
    assert entries[0]["action"] == "deleted task"
    assert entries[1]["action"] == "created task"


def test_task_activity_returns_only_that_task(client: TestClient) -> None:
    first = client.post("/tasks", json={"title": "First"}).json()
    second = client.post("/tasks", json={"title": "Second"}).json()
    client.patch(f"/tasks/{first['id']}", json={"priority": "High"})
    client.patch(f"/tasks/{second['id']}", json={"priority": "Low"})

    response = client.get(f"/tasks/{first['id']}/activity")

    assert response.status_code == 200
    entries = response.json()
    assert len(entries) == 2
    assert all(entry["task_id"] == first["id"] for entry in entries)
