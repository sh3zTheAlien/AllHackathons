# Backend

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Server runs at `http://localhost:8000`.

- `GET /health` — `{"status": "ok"}`
- `GET /ping` — `"Pong!"`
