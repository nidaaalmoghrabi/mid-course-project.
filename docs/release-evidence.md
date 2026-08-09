# Release Evidence

## Baseline

- Branch: final-project
- Date:2026-08-08
- Local app run command: `uvicorn app.main:app --reload --port 8000`
- /health result: HTTP 200 with {"status":"ok","timestamp":"2026-08-08T20:36:41.078094Z"}
- Frontend check: Opened http://127.0.0.1:8000 in a browser and confirmed the task board UI rendered, demo tasks were visible, and browser devtools showed network requests to `/tasks` returning HTTP 200.
- Test command: `pytest -v`
- Test result: 30 passed, 5 warnings in 0.23s

## CI evidence

- Workflow file: `.github/workflows/ci.yml` 
- Trigger: `push` to any branch and `pull_request` against `main`
- Python version: `3.11` via `actions/setup-python@v5`
- Dependency installation: `python -m pip install --upgrade pip` and `pip install -r requirements.txt`
- Test command used by CI: `pytest -v --tb=short`
- Shortcut check:confirmed **no** `continue-on-error`, **no** `|| true`, pytest is **not** skipped or conditionally gated, and the Python version is pinned explicitly (`3.12`, via `actions/setup-python@v5` with `python-version: "3.12"`) rather than left unspecified.

## Docker evidence

- Build command: `docker build -t task-tracker .`
- Run command: `docker run --rm -p 8000:8000 task-tracker`
- /health check: Not run inside a container in this environment; equivalent host check returned HTTP 200 with {"status":"ok","timestamp":"2026-08-08T20:36:41.078094Z"} while the app was served by Uvicorn on the host.
- Non-root check: Implemented — the `Dockerfile` creates a non-root `app` user and switches to it (`USER app`).
- No-baked-secrets check: `.dockerignore` contains `.env` and `.env.*`, and the `Dockerfile` does not copy dotfiles by default; therefore `.env` is excluded from the image build (verify in your CI/build environment as needed).

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
| ------------- | ------------- | ------ | ------------------- |
| Local API runs with `uvicorn app.main:app --reload --port 8000` | Ran the command locally | Correct | None |
| `/health` endpoint returns HTTP 200 | `curl http://127.0.0.1:8000/health` returned HTTP 200 with {"status":"ok","timestamp":"2026-08-08T20:36:41.078094Z"} | Correct | None |
| Test suite runs with `pytest -v` | `python -m pytest -q` returned `30 passed, 5 warnings` | Correct | None |