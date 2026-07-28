# Mini Architecture Decision Record

## Status

Proposed

## Context

The existing FastAPI and vanilla JavaScript Task Tracker needs two small end-to-end features:

1. Due dates with an overdue filter
2. A simple activity log

The implementation must remain suitable for the current project scope. The application uses in-memory storage and does not include authentication, user accounts, notifications, real-time updates, or a production database.

## Decision

### Due Dates and Overdue Filtering

I will add an optional `due_date` field to the task create, update, and response models. The due date will use a date value rather than a date-and-time value because the feature only needs to identify the day on which a task is due.

Overdue status will be calculated rather than stored. A task will be considered overdue when:

* Its due date is before the current date.
* Its status is not `Done`.

Tasks due today will not be considered overdue, and completed tasks will not be marked as overdue.

The backend will support an optional overdue query parameter:

`GET /tasks?overdue=true`

The frontend will include:

* A due-date input in the task form
* A Due pill for tasks with future or current due dates
* An Overdue pill or red indicator for overdue tasks
* An Overdue only filter

### Activity Log

I will add a simple in-memory activity record to track meaningful task actions. Activity events will be created when a task is:

* Created
* Updated
* Moved to a different status
* Deleted

Each activity record will contain a simple identifier, the related task identifier, an action or message, and a timestamp.

The backend will provide endpoints for viewing recent activity and task-specific activity:

* `GET /activity`
* `GET /tasks/{task_id}/activity`

The frontend will display recent events in a small, readable activity panel. The activity log will be read-only. Users will not be able to edit or delete individual activity records.

## Alternatives Considered

### Store an `is_overdue` Boolean

AI suggested storing an `is_overdue` Boolean on every task.

I rejected this approach because the value could become incorrect as the current date changes. For example, a task that is not overdue today may become overdue tomorrow without the stored value being updated. Calculating overdue status from `due_date`, task status, and the current date will maintain one source of truth.

### Calculate Overdue Status Only in the Frontend

Another option was to perform all overdue calculations in JavaScript.

I rejected this because the backend also needs to support overdue filtering. Keeping the overdue rule in the backend will make the behavior consistent for API users and the frontend.

### Add Reminders or Notifications

AI suggested expanding due dates to include reminders or notifications.

I rejected this because notifications, background scheduling, and user preferences are outside the project scope. The feature will only display due dates and identify overdue tasks.

### Build a Complete Audit System

AI suggested a more complex audit system with users, persistent database records, complete before-and-after task snapshots, detailed event metadata, and a separate service for formatting timestamps.

I rejected this because the current application does not include authentication or a production database. A complete audit system would add unnecessary complexity. A small in-memory activity log will be sufficient for demonstrating the feature.

### Add Real-Time Activity Updates

WebSockets or automatic real-time updates were also considered.

I rejected this because real-time communication is outside the project scope. The activity panel will update when the frontend reloads its data after a task action.

## Consequences

The planned implementation will keep both features small and consistent with the existing architecture.

Calculating overdue status will avoid duplicated or stale data. The activity log will provide useful visibility into task changes without introducing authentication, database persistence, or real-time infrastructure.

Because the application uses in-memory storage, tasks and activity records will be lost when the server restarts. This limitation is acceptable for the current project scope.

Additional backend tests and manual browser checks will be required to verify due-date validation, overdue rules, filtering, activity creation, and frontend display behavior.
