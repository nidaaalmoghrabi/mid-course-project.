# Task Tracker API

Task Tracker API is a small REST API learning project built with Python and FastAPI. This first module provides a structured FastAPI application and a health-check endpoint without authentication, database storage, or deployment infrastructure.

## Requirements

- Python 3.10 or newer
- `pip`

## Project Structure

```text
task-tracker-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── repository.py
│   └── routes.py
│
├── tests/
│   ├── __init__.py
│   └── test_health.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Create a Virtual Environment

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows PowerShell

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
py -m venv venv
venv\Scripts\activate.bat
```

After activation, the terminal normally displays `(venv)` before the command prompt.

## Install Dependencies

Upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configure Environment Variables

Copy the example environment file.

### Linux/macOS

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item ".env.example" ".env"
```

The default configuration is:

```dotenv
PORT=8000
APP_ENV=development
```

## Start the Development Server

Run the following command from the project root:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

The automatic Swagger UI documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

The OpenAPI schema will be available at:

```text
http://127.0.0.1:8000/openapi.json
```

## Test the Health Endpoint with curl

Keep the Uvicorn server running and open another terminal.

Run:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "timestamp": "2026-07-20T19:30:15.245721Z"
}
```

The exact timestamp will be different for every request.

To include the response headers, run:

```bash
curl -i http://127.0.0.1:8000/health
```

The response should include:

```text
HTTP/1.1 200 OK
```

## Run the Automated Tests

From the project root, run:

```bash
pytest
```

For more detailed output, run:

```bash
pytest -v
```

## Stop the Server

Press:

```text
Ctrl+C
```

in the terminal where Uvicorn is running.