Prompt 1 — Planning the data model

Prompt used

You are a senior Python backend engineer helping me extend an existing FastAPI Task Tracker.

Current project:

The backend uses FastAPI, Pydantic v2, and in-memory storage.
Tasks currently contain id, title, description, status, priority, and assignee.
Status values are exactly ToDo, InProgress, and Done.
The existing CRUD routes and status-transition rules must continue to work.

I want to add due-date support.

Before writing code, propose a small implementation plan covering:

The field and type to add to the create, update, and response models.
How a task should be classified as overdue.
Whether overdue status should be stored or calculated.
Which existing files will need changes.
Important edge cases to test.

Constraints:

The due date must be optional.
Do not add a database, scheduler, notification system, authentication, or background tasks.
Do not change unrelated task fields or existing status-transition behavior.
Treat your answer as a draft that I will review before coding.

Do not generate code yet.

AI response summary

AI suggested adding an optional due_date field to the task models. It identified create, update, response, storage, route, test, and frontend changes. It also proposed storing an is_overdue Boolean on each task to make frontend rendering easier.

My decision

I accepted the optional due_date field and the suggested file-by-file plan. I rejected storing is_overdue because its value could become stale as the current date changes. I decided that overdue status would be calculated from the task’s due date, current date, and status.

I also clarified that a task is overdue only when:

due_date is before today
AND
status is not Done

This corrected the assumption that every task with a past due date should be considered overdue.

Prompt 2 — Backend implementation and tests

Prompt used

You are helping me make one focused backend change in my existing FastAPI Task Tracker.

Context files:

app/models.py
app/storage.py
app/main.py
tests/test_tasks.py

Add backend support for due dates and overdue filtering.

Exact requirements:

Add due_date: date | None = None to the task create model.
Add an optional due-date field to the task update model.
Include due_date in task responses.
Preserve create and update behavior when no due date is supplied.
Extend GET /tasks with:
overdue: bool | None = None
When overdue=true, return only tasks whose due date is before today and whose status is not Done.
Preserve the existing status and priority filtering behavior.
An empty result must return HTTP 200 with [].

Add focused pytest tests for:

Creating a task with a valid due date
Creating a task without a due date
Updating a due date
Filtering overdue tasks
Excluding completed past-due tasks

Constraints:

Use Pydantic v2 syntax.
Use the existing FastAPI app and in-memory storage.
Do not create a second app instance.
Do not add an ORM, database, notifications, or scheduled jobs.
Do not rewrite unrelated routes.

First explain the planned edits file by file. Then provide the smallest required changes.

AI response summary

AI proposed changes to the Pydantic create, update, and response models, along with storage and route changes for the optional overdue query parameter. It also drafted focused tests for due-date creation, due-date updates, and overdue filtering.

The first draft treated any past-due task as overdue and risked replacing parts of the existing filtering logic.

My decision

I accepted the model structure, optional date type, query parameter, and test ideas after checking them against the existing project files.

I edited the overdue condition so completed tasks were excluded:

task.due_date < date.today() and task.status != TaskStatus.DONE

I also preserved the existing status and priority filters rather than replacing them with a separate filtering path.

I ran the focused tests before moving to the frontend. This followed the Module 2 rule that each backend change should be verified before the next step.

Prompt 3 — Frontend integration

Prompt used

You are helping me extend the existing vanilla HTML, CSS, and JavaScript frontend of my FastAPI Task Tracker.

Context files:

frontend/index.html
app/main.py
app/models.py

The backend already supports:

due_date: optional date
GET /tasks?overdue=true

Add the due-date feature to the existing frontend in small changes.

Required behavior:

Add a Due date input to the existing create/edit modal.
Send the due date in POST and PATCH requests.
When editing, populate the input with the saved value.
Show a Due pill for a task with a current or future due date.
Show an Overdue pill and red visual indicator when the due date is before today and status is not Done.
Add an Overdue only control.
The control must request:
GET /tasks?overdue=true
Turning off the filter must reload the normal task list.
Preserve the existing Kanban columns, priority sorting, modal validation, drag-and-drop, and error handling.

Constraints:

Do not add a frontend framework or build tool.
Do not rewrite the whole frontend file.
Do not duplicate backend filtering by downloading all tasks and filtering them only in JavaScript.
Show the selected sections that should change and explain each change before providing code.

AI response summary

AI suggested adding a date input to the modal, displaying the due date on task cards, calculating overdue status in JavaScript, and filtering the already-loaded task array in the frontend.

It also proposed Due and Overdue pills and a visual style for overdue cards.

My decision

I accepted the due-date input, modal population, request payload changes, card pill, and overdue visual indicator.

I rejected frontend-only filtering because the backend already supported GET /tasks?overdue=true. The final Overdue only button calls the backend filter, avoiding duplicated filter behavior.

I kept a small frontend calculation only for deciding which visual pill to display. The backend remained responsible for query filtering and model validation.

Feature 2: Activity log
Prompt 1 — Activity design

Prompt used

You are a senior FastAPI engineer helping me plan a second scoped feature for an existing Task Tracker.

Current project:

FastAPI backend
Pydantic v2 models
In-memory task storage
Vanilla HTML, CSS, and JavaScript frontend
Existing task CRUD and status-transition validation
No authentication, users, database, real-time updates, notifications, or deployment work

I want to add a small activity log.

The log should record:

Task creation
Actual field updates
Status changes
Task deletion

Propose a minimal design that includes:

A simple in-memory activity record.
An endpoint for recent activity.
An endpoint for activity belonging to one task.
Readable activity wording.
Where events should be created in the existing CRUD flow.
Focused tests.

Desired endpoints:

GET /activity
GET /tasks/{task_id}/activity

Constraints:

Keep the design small and readable.
Do not add a database-backed audit system.
Do not add users, permissions, event rollback, event restoration, real-time updates, or external logging services.
Do not generate code yet.
List assumptions that I should review before implementation.

AI response summary

AI suggested an activity model containing an event identifier, task identifier, action description, and timestamp. It proposed a general activity endpoint and a task-specific endpoint.

It also suggested recording create, update, status-change, and delete events. A more advanced alternative included persistent audit tables, user identities, event categories, rollback support, and restored deleted-task snapshots.

My decision

I accepted the small in-memory event model, readable descriptions, and the two endpoints.

I rejected a database-backed audit architecture, user tracking, rollback, event restoration, and real-time delivery because they were too complex and outside the course scope.

I accepted that activity would be lost when the application restarts because the existing task system also uses in-memory storage.

Prompt 2 — Update event wording and changed fields

Prompt used

I implemented activity events for task updates, but the current result is incorrect.

Evidence:

The frontend submits the complete edit form.
I changed only the assignee.
The activity log reported several submitted fields even though their stored values did not change.

Relevant files:

app/main.py
app/storage.py
app/models.py
tests/test_tasks.py

Required behavior:

Save or inspect the original task before applying the update.
Compare the original values with the final updated values.
Record only fields whose values actually changed.
Use readable labels such as:
updated assignee
updated due date
Treat status separately using:
changed status from ToDo to InProgress
Do not report unchanged fields merely because they were present in the PATCH body.
Preserve existing update validation and status-transition rules.

Add or update a focused pytest test proving that when only the assignee changes, no other field appears in the activity description.

Do not suppress the issue or weaken the test. Explain the cause first, then propose the smallest correction.

AI response summary

AI identified that the update logic was using the submitted PATCH fields as evidence of change. Because the frontend sends existing values as part of the edit form, the log incorrectly described unchanged fields as updated.

AI proposed capturing the task’s original values, applying the update, and comparing the original and final versions before building the activity description.

My decision

I accepted the before-and-after comparison approach.

I rejected the original implementation that treated every submitted field as changed. I added a focused test to prove that changing only the assignee produces only:

updated assignee

I also kept status changes separate so they retain the clearer from/to format.

This was an important review correction because the original AI-generated behavior looked reasonable in code but did not accurately describe the user’s action. The modules emphasize debugging from exact evidence rather than accepting plausible output.

Prompt 3 — Frontend activity panel

Prompt used

You are helping me add a small activity view to the existing Task Tracker frontend.

Context files:

frontend/index.html
app/main.py

Available backend endpoints:

GET /activity
GET /tasks/{task_id}/activity

Add a compact activity panel to the right side of the existing Kanban board.

Required behavior:

Load recent general activity when the page opens.
Add an All button that reloads GET /activity.
Add an Activity button to each task card.
Clicking a task’s Activity button must call:
GET /tasks/{task_id}/activity
Display readable event descriptions and timestamps.
Show a clear empty state when no activity exists.
Show a readable error when the request fails.
Refresh the activity panel after create, edit, status change, or delete operations.

Layout constraints:

Keep the panel smaller than the Kanban board.
Do not replace the board or open a large new page.
Preserve the three status columns.
Keep the existing Edit button.
Make Edit, Activity, and Delete buttons compact enough to remain on one row.
Ensure long task titles and descriptions wrap inside their cards.
Do not add React, Vue, Bootstrap, or another frontend dependency.

First provide a short implementation plan. Then show only the sections that need changes.

AI response summary

AI suggested a compact activity panel with a heading, loading and empty states, an All button, and task-specific Activity controls. It also proposed refreshing activity after successful task operations.

The first layout draft made the supporting controls and panel too large relative to the Kanban board.

My decision

I accepted the compact right-side panel, All button, task-specific Activity buttons, loading behavior, and automatic refresh after task operations.

I edited the styling so the activity panel remained secondary to the board. I reduced the size of Edit, Activity, and Delete buttons and kept them on one line.

I also fixed the card width and wrapping so long titles and descriptions did not stretch the columns. The modal was reduced in size to keep the interface readable.