@echo off
echo Starting FastAPI Enterprise Backend via Python Module...
python -m uvicorn backend:app --reload --port 8000
cmd