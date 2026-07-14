# Backend

```bash
cd backend
source env/bin/activate
pip install -r requirements.txt
flask --app main run --reload
```

Keeping requriements.txt file up to date with pipreqs:
```pipreqs . --force --mode no-pin```


Server runs at `http://localhost:5000`.


- `GET /health` — `{"status": "ok"}`
- `GET /ping` — `"Pong!"`
