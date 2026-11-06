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
