# Comments on Tasks Feature Plan

## 1. Data Model

Add comment schemas to [app/models.py](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/app/models.py:31), alongside the existing Pydantic request/response models.

- Add `CommentCreate` with `author` and `body` only.
- Add `CommentResponse` with `id`, `task_id`, `author`, `body`, and `created_at`.
- Follow the repo's existing model convention: `BaseModel`, `ConfigDict(extra="forbid")`, and `field_validator` validation.
- Generate `id` and `created_at` in [app/storage.py](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/app/storage.py:32), matching task/activity UUID and UTC timestamp behavior.
- Store comments separately from `TaskResponse` so existing `/tasks` response shape does not change.
- Add an in-memory comment collection in `app/storage.py`, likely keyed by comment UUID or stored as a list filtered by `task_id`.

## 2. API Routes

Add task-nested comment routes in [app/main.py](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/app/main.py:111), because task and activity routes currently live there.

- `GET /tasks/{task_id}/comments`
  - Request body: none.
  - Response body: list of comment responses.
  - Recommended order: oldest first, unless the team prefers newest first.
  - Error cases: `404` if the task does not exist, unless the team intentionally mirrors task activity's historical behavior.

- `POST /tasks/{task_id}/comments`
  - Request body: `author`, `body`.
  - Response body: created comment with `id`, `task_id`, `author`, `body`, `created_at`.
  - Status: `201 Created`.
  - Error cases: `404` for missing task; `422` for missing, blank, oversized, or unknown fields.

Use the existing missing-task detail style: `Task with id {task_id} not found`.

## 3. Tests

Add tests using the existing `TestClient` fixture and storage reset pattern in [tests/conftest.py](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/tests/conftest.py:8). These could live in `tests/test_comments.py` or in [tests/test_tasks.py](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/tests/test_tasks.py:4).

Happy path:

- `test_create_comment_for_task_returns_201_with_generated_fields`
- `test_list_task_comments_empty_returns_200_and_empty_list`
- `test_list_task_comments_returns_comments_for_that_task_only`
- `test_list_task_comments_returns_comments_in_expected_order`

Validation:

- `test_create_comment_missing_author_returns_422`
- `test_create_comment_blank_author_returns_422`
- `test_create_comment_author_over_100_returns_422`
- `test_create_comment_missing_body_returns_422`
- `test_create_comment_blank_body_returns_422`
- `test_create_comment_body_over_2000_returns_422`
- `test_create_comment_unknown_field_returns_422`
- `test_create_comment_rejects_client_generated_fields`

Edge cases:

- `test_create_comment_missing_task_returns_404_with_detail`
- `test_list_comments_missing_task_returns_404_with_detail`
- `test_comment_created_at_is_timezone_aware_utc`
- `test_delete_task_removes_or_retains_comments_according_to_policy`

## 4. Frontend Changes

Change [frontend/index.html](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/frontend/index.html:583), since the frontend is a single vanilla HTML/CSS/JS file.

- Add a `Comments` action on each task card near `Edit`, `Activity`, and `Delete`.
- Add a comments modal or task-focused panel that shows the selected task title, existing comments, and an add-comment form.
- Show each comment's author, body, and formatted `created_at`.
- Add `author` input and `body` textarea with client-side required and max-length validation.
- Fetch comments from `GET /tasks/{task_id}/comments` when opening the comments UI.
- Submit new comments to `POST /tasks/{task_id}/comments`, then refresh or append the created comment.
- Reuse existing frontend patterns: `API_BASE_URL`, `escapeText`, status messages, modal styling, and server-error rendering where practical.

## 5. Migration Notes

No database migration is visible because this repo intentionally uses process-local in-memory storage, documented in [AGENTS.md](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/AGENTS.md:7) and [README.md](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/README.md:3).

- Add comment state to `app/storage.py`; update `storage._reset()` so tests clear comments too.
- Do not change existing task response bodies unless the team explicitly wants comment counts or embedded comments.
- Demo tasks seeded in `app/main.py` would start with no comments.
- Existing runtime data is already non-durable and lost on restart.
- Decide whether deleting a task cascades comment deletion. This is a data-shape decision even without a database.

## 6. Open Questions

- Should comments be deleted when their task is deleted, or retained like activity history?
- Should comment creation add an activity entry such as `added comment`?
- Should `author` be free text, or reserved for a future authenticated user model?
- Should body whitespace be preserved exactly, or trimmed after validation?
- Should comments be oldest-first for conversation reading or newest-first for recent updates?
- Should comments support markdown, links, mentions, or plain text only?

## Files read

- [AGENTS.md](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/AGENTS.md:5)
- [README.md](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/README.md:49)
- [app/models.py](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/app/models.py:31)
- [app/main.py](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/app/main.py:111)
- [app/routes.py](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/app/routes.py:1)
- [app/storage.py](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/app/storage.py:9)
- [app/repository.py](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/app/repository.py:1)
- [app/business_rules.py](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/app/business_rules.py:1)
- [tests/conftest.py](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/tests/conftest.py:8)
- [tests/test_tasks.py](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/tests/test_tasks.py:4)
- [tests/test_health.py](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/tests/test_health.py:1)
- [frontend/index.html](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/frontend/index.html:658)
- [docs/midcourse/storage-decision.md](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/docs/midcourse/storage-decision.md:1)
- [docs/midcourse/mini-adr.md](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/docs/midcourse/mini-adr.md:1)
- [docs/midcourse/user-stories.md](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/docs/midcourse/user-stories.md:1)
- [docs/midcourse/verification.md](C:/Users/beaut/OneDrive/Desktop/Python/task-tracker-api/docs/midcourse/verification.md:1)

## Assumptions to verify

- Assumption: comment edit/delete is out of scope for the first version.
- Assumption: comments should not be embedded in task responses.
- Assumption: missing-task comment routes should return `404`, even though task activity can remain visible after deletion.
- Assumption: no authentication or database should be introduced for this feature.
