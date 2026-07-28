# Verification Evidence

## 1. Baseline Check

Before adding the two selected features, I checked that the existing Task Tracker still worked.

Commands:

```powershell
uvicorn app.main:app --reload
pytest
```

Baseline observations:

```text
PASS: FastAPI server started successfully

PASS: GET /health returned HTTP 200

PASS: Swagger documentation opened at http://127.0.0.1:8000/docs

PASS: existing task CRUD endpoints were available

PASS: existing Kanban board loaded in the browser

NOTE: the exact baseline pytest count was not recorded
```

The baseline project did not yet include:

```text
due_date support

GET /tasks?overdue=true

Due and Overdue pills

Overdue only frontend filter

GET /activity

GET /tasks/{task_id}/activity

Frontend activity panel

Frontend Delete button
```

---

## 2. Backend Test Results

After implementing due dates, overdue filtering, and the activity log, I ran the complete pytest suite.

Command:

```powershell
pytest
```

Final result:

```text
30 passed
```

Warnings:

```text
4 FastAPI/Starlette deprecation warnings

No tests failed
```

The new backend tests covered:

```text
PASS: task created with a due date

PASS: task due date updated

PASS: overdue filtering returned overdue tasks

PASS: completed tasks were excluded from overdue results

PASS: task creation generated an activity event

PASS: task update generated an activity event

PASS: update activity included only fields that actually changed

PASS: status-change activity included the previous and new status

PASS: task deletion generated an activity event

PASS: task-specific activity endpoint returned the correct events
```

The warnings were not changed because they were unrelated to the two selected features and did not affect the test results.

---

## 3. Manual Browser Checks

### Feature 1: Due dates and overdue filter

```text
PASS: Due date input appeared in the create/edit modal

PASS: a task could be created without a due date

PASS: a task could be created with a valid due date

PASS: a future or current due date displayed a Due pill

PASS: a past due date on an incomplete task displayed an Overdue pill

PASS: overdue cards received a red visual indicator

PASS: editing a task displayed its saved due date

PASS: updating a due date changed the value shown on the card

PASS: a completed task with a past due date was not marked overdue

PASS: clicking Overdue only requested GET /tasks?overdue=true

PASS: only overdue incomplete tasks appeared while the filter was active

PASS: disabling the filter restored the complete board
```

### Feature 2: Activity log

```text
PASS: creating a task displayed "created task"

PASS: changing only the assignee displayed "updated assignee"

PASS: unchanged fields were not included in the activity description

PASS: changing only the due date displayed "updated due date"

PASS: changing status displayed the previous and new status

PASS: the All button displayed general activity

PASS: each task card contained an Activity button

PASS: the Activity button displayed only that task's events

PASS: deleting a task removed the card from the board

PASS: deleting a task displayed "deleted task"

PASS: the activity panel refreshed after task operations
```

### Frontend layout checks

```text
PASS: task cards remained inside their Kanban columns

PASS: long titles wrapped instead of stretching the card

PASS: long descriptions wrapped correctly

PASS: Edit, Activity, and Delete buttons appeared on one line

PASS: the buttons remained usable after their size was reduced

PASS: the smaller create/edit modal still worked correctly

PASS: the activity panel remained readable without replacing the Kanban board
```

---

## 4. Behavior Contract Before Refactor

Before changing card widths, text wrapping, button sizes, button layout, and modal size, I recorded the behaviors that had to remain unchanged.

```text
PASS: GET /health returned HTTP 200

PASS: existing tasks could still be created without a due date

PASS: tasks could be created and updated with a due date

PASS: task edits preserved unrelated field values

PASS: drag-and-drop status changes persisted through the API

PASS: invalid status transitions continued to be rejected

PASS: incomplete tasks with past due dates were marked overdue

PASS: completed tasks were not marked overdue

PASS: GET /tasks?overdue=true returned only overdue incomplete tasks

PASS: activity events described only actual changes

PASS: status events included both previous and new statuses

PASS: task-specific activity returned only events for the selected task

PASS: deleting a task removed it and recorded a deletion event
```

Result:

```text
13/13 behavior checks passed before refactoring
```

A working checkpoint was committed before the focused frontend refactor.

---

## 5. Behavior Contract After Refactor

After changing the frontend layout, I repeated the same behavior contract.

```text
PASS: GET /health returned HTTP 200

PASS: existing tasks could still be created without a due date

PASS: tasks could be created and updated with a due date

PASS: task edits preserved unrelated field values

PASS: drag-and-drop status changes persisted through the API

PASS: invalid status transitions continued to be rejected

PASS: incomplete tasks with past due dates were marked overdue

PASS: completed tasks were not marked overdue

PASS: GET /tasks?overdue=true returned only overdue incomplete tasks

PASS: activity events described only actual changes

PASS: status events included both previous and new statuses

PASS: task-specific activity returned only events for the selected task

PASS: deleting a task removed it and recorded a deletion event
```

Result:

```text
13/13 behavior checks passed after refactoring

30 pytest tests passed
```

The card-width, wrapping, button-size, button-layout, and modal-size changes did not alter the required application behavior.

---

## 6. Break Test 1 — Overdue Detection

Purpose:

```text
Prove that the overdue test detects a bug when completed tasks are incorrectly treated as overdue.
```

Correct production behavior:

```python
task.due_date < date.today() and task.status != TaskStatus.DONE
```

Temporary broken behavior:

```python
task.due_date < date.today()
```

Focused command:

```powershell
pytest tests/test_tasks.py -k "overdue" -v
```

Expected result:

```text
A completed task with a past due date is incorrectly returned by the overdue filter.

The overdue test must fail.
```

Break Test result:

```text
FAIL detected as expected: the test found that a completed past-due task was incorrectly included in the overdue results.
```

Restoration:

```text
The status != TaskStatus.DONE condition was restored.
```

Verification after restoration:

```text
PASS: focused overdue tests passed

PASS: full pytest suite passed — 30 passed
```

---

## 7. Break Test 2 — Activity Changed Fields

Purpose:

```text
Prove that the activity test detects misleading update descriptions.
```

Correct production behavior:

```text
The task values before and after the update are compared.

Only fields whose values actually changed are included in the activity message.
```

Temporary broken behavior:

```text
The update activity logic was changed to report every field submitted by the frontend.
```

Focused command:

```powershell
pytest tests/test_tasks.py -k "changed_fields" -v
```

Expected result:

```text
When only the assignee changes, unchanged fields incorrectly appear in the activity message.

The changed-fields test must fail.
```

Break Test result:

```text
FAIL detected as expected: the test found unchanged fields in the activity description.
```

Restoration:

```text
The before-and-after value comparison was restored.
```

Verification after restoration:

```text
PASS: changed-fields activity test passed

PASS: full pytest suite passed — 30 passed
```

---

## 8. Final Verification Summary

```text
PASS: baseline application was checked before feature work

PASS: both selected features were implemented in the backend

PASS: both selected features were visible and usable in the frontend

PASS: new backend tests covered due dates, overdue behavior, and activity events

PASS: complete pytest suite passed with 30 tests

PASS: manual browser checks were completed

PASS: behavior contract passed before and after refactoring

PASS: two Break Tests proved that important tests detect broken behavior

NOTE: 4 deprecation warnings remained, but no tests failed
```
