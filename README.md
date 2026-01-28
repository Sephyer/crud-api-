# CRUD API (FastAPI + Postgres)

A small CRUD REST API built with **FastAPI** and **SQLAlchemy**. It exposes endpoints to create, read, update, and delete `Item` records stored in a database (recommended: **PostgreSQL**).

Even if you were expecting something like Flask, this project is the FastAPI equivalent: same “Python web API” idea, but using FastAPI + Uvicorn instead of Flask + Gunicorn.

## Tech / components used

- **FastAPI**: Web framework for the API
- **Uvicorn**: ASGI server used to run the app
- **SQLAlchemy**: ORM + DB engine
- **PostgreSQL** (recommended): Database backend
- **psycopg2-binary**: Postgres driver used by SQLAlchemy
- **python-dotenv**: Loads environment variables from a `.env` file

## Project structure

```
app/
  main.py       # FastAPI app + routes
  database.py   # DB engine/session setup; loads DATABASE_URL from .env
  models.py     # SQLAlchemy models (Item)
  schemas.py    # Pydantic schemas (ItemCreate/Item)
  crud.py       # CRUD functions
```

## Prerequisites

- Python 3.10+ (3.11+ recommended)
- A running Postgres instance (local install or Docker)
  - Note: if you have multiple Pythons installed (ex: 3.14 preview), use `py -3.12` or `py -3.10` to create your venv.

## Configuration (.env)

This app uses a `DATABASE_URL` environment variable (optionally loaded from a `.env` file in the project root).

Create a file named `.env` next to `requirements.txt`:

```env
# Example (Postgres)
DATABASE_URL=postgresql+psycopg2://crud:crud@localhost:5432/crud
```

Notes:
- `.env` is ignored by git (see `.gitignore`).
- If `DATABASE_URL` is missing, the app defaults to SQLite at `sqlite:///./test.db`.
- See `.env.example` for ready-to-copy examples.

## Run locally (Windows PowerShell)

From the project root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Optional: confirm your `.env` loads correctly:

```powershell
python .\test_env.py
```

Start the API:

```powershell
python -m app.main
```

Then open:
- Interactive docs (Swagger): `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Run with Docker Compose (API + Postgres)

This is the easiest “one command” way to run both the API and Postgres together:

```powershell
docker compose up --build
```

Then open:
- Interactive docs (Swagger): `http://127.0.0.1:8000/docs`

To stop:

```powershell
docker compose down
```

## Run Postgres with Docker (quick start)

If you don’t already have Postgres running:

```powershell
docker run --name crud-postgres `
  -e POSTGRES_USER=crud `
  -e POSTGRES_PASSWORD=crud `
  -e POSTGRES_DB=crud `
  -p 5432:5432 `
  -d postgres:16
```

Use this in your `.env`:

```env
DATABASE_URL=postgresql+psycopg2://crud:crud@localhost:5432/crud
```

## API endpoints

- `GET /` — basic info
- `GET /health` — health check
- `GET /items` — list items (`skip`, `limit`)
- `POST /items` — create an item
- `GET /items/{item_id}` — fetch a single item
- `PUT /items/{item_id}` — replace an item (full update)
- `PATCH /items/{item_id}` — update an item (partial update)
- `DELETE /items/{item_id}` — delete an item

## Example requests (curl)

### PowerShell (recommended)

Create an item:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/items" -ContentType "application/json" -Body '{"name":"Widget","description":"Example item"}'
```

Get it back:

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/items/1"
```

Update it:

```powershell
Invoke-RestMethod -Method Put -Uri "http://127.0.0.1:8000/items/1" -ContentType "application/json" -Body '{"name":"Widget v2","description":"Updated"}'
```

Delete it:

```powershell
Invoke-RestMethod -Method Delete -Uri "http://127.0.0.1:8000/items/1"
```

### curl (macOS/Linux) or curl.exe (Windows)

Create an item:

```bash
curl -X POST "http://127.0.0.1:8000/items" \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget","description":"Example item"}'
```

Get it back:

```bash
curl "http://127.0.0.1:8000/items/1"
```

Update it:

```bash
curl -X PUT "http://127.0.0.1:8000/items/1" \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget v2","description":"Updated"}'
```

Delete it:

```bash
curl -X DELETE "http://127.0.0.1:8000/items/1"
```

## Notes / gotchas

- Tables are created automatically at startup via `models.Base.metadata.create_all(bind=engine)` in `app/main.py`.
- If you use `docker compose up --build`, the API is configured to talk to Postgres at `db:5432` automatically.
