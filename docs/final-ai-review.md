# Final AI Review and Ownership Evidence

## AGENTS.md guardrails
- Repo-specific stack and commands included: yes — `AGENTS.md` lists exact install/run/test commands for the `app/` and `frontend/` components.
- Docs-first/read-first guardrail included: yes — "Module 5 guardrails" section states "Work docs-first and read-only by default" and "make required edits in `docs/` first."
- Unexpected app/frontend edits rule included: yes — "Do not change application code unless explicitly approved... Flag unexpected application changes, broadened scope, new dependencies, or data-model changes before proceeding."

## AI code review mini-log
| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| Add `README.md` final section with exact run/test/Docker commands | Useful | It matches repo structure and course expectations | Verified against existing `README.md`, `Dockerfile`, `.github/workflows/ci.yml`, and repo files |
| Confirm CI shortcut safety and runtime commands | Useful | It ensures GitHub Actions will not conceal failed tests | Verified with `.github/workflows/ci.yml` contents and explicit `continue-on-error` / `|| true` absence |
| Replace placeholder security backlog wording | Useful | It made the security review more accurate to the repository | Verified by reading `docs/security-review.md` and aligning the finding content |

## AI security mini-review
| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| CI workflow trigger and shortcut checks | `.github/workflows/ci.yml` | Valid | Workflow uses `push` and `pull_request`, installs dependencies, runs `pytest`, and has no dangerous shortcuts | Document in `docs/release-evidence.md` and keep CI run URL after first push/PR |
| Docker non-root and secrets handling | `Dockerfile`, `.dockerignore` | Valid | `Dockerfile` creates/uses non-root `app` user; `.dockerignore` excludes `.env` and `.env.*` | Note the configured behavior in `docs/release-evidence.md` |
| No auth around task endpoints | `app/main.py`, `README.md` | Valid | API routes are public by design for Module 5, but this is a security/backlog concern | Keep as an unfixed backlog item in `docs/security-review.md` and document scope decisions |

## Manual security check
Confirmed the CI workflow file is present and readable, verified the GitHub Actions steps install dependencies and run `pytest`, and checked the Dockerfile for non-root user configuration. I also inspected `docs/security-review.md` and `docs/release-evidence.md` for accurate evidence statements and no misleading shortcuts.

## One AI output I rejected or corrected
AI suggested a security backlog line about unpinned dependencies. I corrected that to focus on the missing CI workflow trigger and evidence because the repository already has a workflow, and the assignment specifically called for CI and shortcut verification.

## Three AI usage rules
1. Never paste: passwords, API keys, tokens, `.env` values, credentials, production logs, or real personal/customer data.
2. Always verify: AI-generated code, configuration, commands, documentation claims, and security findings against the actual repository and test results.
3. Record AI contributions by: documenting important AI suggestions, my grade or decision, the evidence I used, and whether I accepted, corrected, or rejected the suggestion.

## Ownership statement
I am comfortable submitting this work because the document contents match the repository state, the CI workflow is present and correctly configured, and the Docker evidence reflects the actual project files.
