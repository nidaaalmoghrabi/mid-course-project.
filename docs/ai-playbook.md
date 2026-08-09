# My AI Playbook

## When I reach for AI first
- Scaffolding repetitive, well-understood patterns: a new Pydantic model, a CRUD endpoint, a React component that follows a shape I've already established elsewhere in the project.
- Drafting documentation — user stories, ADRs, this playbook — where the value is in getting a structured first pass fast, then correcting it against what actually happened.
- Debugging with evidence in hand: pasting a failing test plus the relevant code and asking for a diagnosis is much faster than tracing it manually line by line, as long as I verify the fix afterward instead of just applying it.
- Turning a vague idea ("add due dates") into a scoped plan with explicit constraints before I write a single line of code.

## When I do not reach for AI first
- Anything touching data-loss risk or a security boundary (auth, CORS, what gets baked into a Docker image) — I want to reason through this myself first, then use AI as a second opinion, not the first one.
- When I don't yet understand the existing code well enough to judge whether an AI suggestion is even reasonable. If I can't tell good from bad, I'm not ready to accept either.
- Structural or naming decisions that ripple across the whole repo (like the `backend/` vs `app/` question this project raised) — these deserve a deliberate human decision, not a default "yes, sure" to whatever AI proposes first.

## My non-negotiables
- Never paste real secrets, `.env` values, tokens, production logs, or real personal/customer data into any AI tool — test/dummy data only, always.
- Never accept a diff I can't explain back in my own words. If I can't say what a line does and why, it doesn't go in.
- Never let an AI-drafted rule (in `AGENTS.md` or anywhere else) silently drift out of sync with what the code actually does — if I notice a mismatch, I document it immediately, not "later."

## My review rules
- Run it before I trust it: tests, curl against a live endpoint, an actual browser check — not just reading the diff and nodding.
- Grade AI output like evidence, not like an answer key: Useful / Noise / Wrong, with a reason, every time — not just "looks fine."
- When AI proposes a structural change (rename, restructure, new dependency), I ask myself what it actually fixes versus what it costs to change, before saying yes.
- Read validation and security-relevant logic line by line myself at least once, even if the tests pass — tests can be wrong in the same blind spot the code is.

## What I am still figuring out
- Where the line is between "reasonable scope decision" (like keeping `backend/` instead of renaming to `app/`) and "avoiding a fix because it's inconvenient." I think I got this one right, but I want to keep checking myself on it rather than assuming the first instinct is always correct.
- How much AI-generated documentation to trust as accurate-by-default versus how much to independently re-verify every time — right now I lean toward re-verifying almost everything, which is safe but slow, and I haven't found the right calibration yet.
- How to review AI-suggested infrastructure changes (Docker, CI) as rigorously as I review application code, since I have less hands-on intuition there and it's easier to accept something that "looks standard" without fully understanding it.

## Decision Card

| Situation | My one rule |
|---|---|
| New feature | Write the user story and acceptance criteria before any code — including at least one AI assumption I expect to correct. |
| Code review | Grade every AI comment Useful / Noise / Wrong with a reason before acting on any of them. |
| Debugging | Give AI the failing test and the real error, not a description of the problem from memory. |
| Infrastructure (CI/Docker) | Read every line before running it — infrastructure mistakes are harder to notice later than application bugs. |
| Never-paste | Real secrets, tokens, `.env` values, and real personal/customer data — no exceptions, no "just this once." |