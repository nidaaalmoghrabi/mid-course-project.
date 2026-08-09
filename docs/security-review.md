# Security Review

## Al Findings

| Severity | File:Line | Finding | Suggested Fix | Grade | Reason |
| --- | --- | --- | --- | --- | --- |
| High | `README.md:3`, `app/main.py:93` | Task data can be listed without authentication or authorization. | Add an authentication/authorization layer before exposing task data outside local learning use. | TODO | TODO |
| High | `README.md:3`, `app/main.py:102`, `app/main.py:125`, `app/main.py:139` | Task create, update, and delete endpoints are unauthenticated. | Require authenticated users and authorize task mutations by role or owner before deployment. | TODO | TODO |
| Medium | `app/main.py:30` | CORS allows broad local origins, `null`, all methods, and all headers. | Restrict CORS origins, methods, and headers to the exact trusted frontend environment before deployment. | TODO | TODO |
| Medium | `requirements.txt:1` | Python dependencies are unpinned. | Pin dependency versions or use a lock file, and update them through a reviewed dependency process. | TODO | TODO |
| Low | `app/main.py:44` | Demo tasks seed automatically outside test runs. | Gate demo seed data behind an explicit development flag so non-development environments start empty. | TODO | TODO |

## My Manual Findings

| Severity | File:Line | Finding | Suggested Fix | Reason |
| --- | --- | --- | --- | --- |

## Reconciliation

### Agreement

TODO

### Al-only

TODO

### You-only

TODO

## Top 3 Unfixed Backlog

| Rank | Finding | Severity | Owner | Next Step |
| --- | --- | --- | --- | --- |
| 1 | Task read and mutation endpoints are unauthenticated. | High | App owner | Decide whether the Module 5 scope should remain local-only or add authentication before any shared deployment. |
| 2 | CORS settings are permissive for local development, including `null`, all methods, and all headers. | Medium | App owner | Replace development CORS settings with an environment-specific allowlist before deployment. |
| 3 | No CI workflow is configured to run tests on pushes or pull requests. | Medium | App owner | Add a CI workflow (for example, GitHub Actions) that runs `python -m pytest` on push and PRs to ensure tests run automatically. |
