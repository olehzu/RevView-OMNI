# RevView-OMNI
Senior design project for TCU class of 2027

## Run it locally

Backend (Python 3.13), from `backend/`:

```
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
pytest
uvicorn app.main:app --reload   # http://127.0.0.1:8000/api/v1/health
```

Frontend (Node 20.19 or newer), from `frontend/`:

```
npm install
npm test
npm run dev
```

## Run the page

The review package page needs the API and the frontend running together, in two terminals:

1. From `backend/`, with the virtual environment active: `uvicorn app.main:app --reload`
2. From `frontend/`: `npm run dev`
3. Open http://localhost:5173/?review=rev-0001 and press Load (the link only fills in the review id)

The frontend's development server forwards `/api` to the API on port 8000. Only `rev-0001` exists, and it is Synthetic Data.

## Checks before pushing

Pull requests to `main` run these checks (`.github/workflows/pull-request.yml`); run them first so a red run is never a surprise.

Backend, from `backend/` with the virtual environment active:

```
ruff format --check .
ruff check .
mypy app tests
pytest
```

Frontend, from `frontend/`:

```
npm run format:check
npm run lint
npm run typecheck
npm test
npm run build
```
