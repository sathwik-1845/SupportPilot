# SupportPilot Backend (FastAPI + PostgreSQL)

## Run it
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # Windows: copy .env.example .env
docker compose up -d             # starts PostgreSQL
uvicorn app.main:app --reload --port 8000
```
- Swagger UI: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health
- DB check: http://localhost:8000/api/v1/health/db
