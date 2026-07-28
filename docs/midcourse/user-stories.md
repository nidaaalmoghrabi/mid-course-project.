Due dates + overdue filter

US1 — Create a task with a due date

As a task-board user, I want to assign an optional due date when creating a task so that I know when it should be completed.

Acceptance criteria:

The create modal contains a Due date field.
The field is optional.
A valid date is stored and returned by the API.
A task without a due date can still be created.
The card displays the saved due date.

US2 — Update a due date

As a task-board user, I want to add, change, or remove a task’s due date so that its deadline stays accurate.

Acceptance criteria:

The edit modal displays the current due date.
A new valid date can replace the existing date.
The due date can be removed.
The updated value appears after the board refreshes.
Updating the due date does not unintentionally change unrelated task fields.

US3 — Identify overdue tasks

As a task-board user, I want overdue tasks to be visually identified so that I can prioritize delayed work.

Acceptance criteria:

A task is overdue only when its due date is before today.
A task with status Done is not marked overdue.
An overdue task shows an Overdue pill.
An overdue task receives a red visual indicator.
A future or current due date shows a normal Due pill.

US4 — Filter overdue tasks

As a task-board user, I want to display only overdue tasks so that I can focus on delayed work.

Acceptance criteria:

GET /tasks?overdue=true returns only overdue tasks.
Completed tasks are excluded even when their dates are in the past.
The Overdue only frontend control uses the backend filter.
An empty result returns HTTP 200 with an empty list.
Turning off the filter restores the normal task board.

Corrected AI assumption

AI initially treated every task with a past due date as overdue. I corrected this so that completed tasks are excluded. The final rule is: due_date < today and status != Done.

Activity log

US1 — Record task creation

As a task-board user, I want task creation to appear in the activity log so that I can see when work was added.

Acceptance criteria:

Creating a task generates one activity event.
The event identifies the related task.
The event contains readable text such as created task.
The event appears in GET /activity.
It also appears in the task-specific activity endpoint.

US2 — Record changed fields only

As a task-board user, I want update activity to list only fields that actually changed so that the log remains accurate and readable.

Acceptance criteria:

Changing only the assignee records updated assignee.
Unchanged submitted fields are not reported.
Changing only the due date records updated due date.
An update does not generate misleading field descriptions.
The event remains associated with the correct task.

US3 — Record status transitions

As a task-board user, I want status changes to show the previous and new status so that I can follow task progress.

Acceptance criteria:

A status update creates an activity event.
The event contains both old and new status values.
The wording follows the format changed status from X to Y.
The status change appears in general and task-specific activity views.
Existing status-transition validation remains enforced.

US4 — View activity in the frontend

As a task-board user, I want to view all activity or activity for one task so that I can understand recent changes.

Acceptance criteria:

A readable activity panel appears beside the board.
The All button loads general activity.
Each task card contains an Activity button.
The task Activity button loads only events for that task.
Empty or failed activity requests are handled clearly.

US5 — Record deletion

As a task-board user, I want deleted tasks to leave an activity record so that deletion is still traceable.

Acceptance criteria:

Deleting a task calls DELETE /tasks/{id}.
A deleted task event is generated.
The board refreshes after successful deletion.
The deleted card is removed.
The deletion event remains available in the general activity feed.

Corrected AI assumption

AI originally compared the complete submitted update payload and produced activity entries for fields whose values had not changed. I corrected the implementation to compare stored values before and after the update and record only actual differences.