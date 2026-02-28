Technology Stack (Final)
Backend

Python 3.10+

FastAPI

SQLite (single-file DB, zero cost)

Data & NLP

Pandas

NumPy

NLTK (VADER)

LLM

API-based (lightweight model)

JSON-structured responses only

Frontend

Vanilla HTML, CSS, JavaScript

Chart.js


## how it runs ##
1. Scrape ratings
2. Scrape social posts
3. Run VADER on all posts
4. Select high-impact posts
5. Call LLM for refinement
6. Aggregate sentiment
7. Normalize ratings
8. Compute weekly score
9. Store results
10. Update leaderboard

## quick start ##
1. Initialize DB schema:
   `python -m db.init_db`
2. Seed starter players:
   `python -m db.seed_players`
3. Run API:
   `uvicorn api.main:app --reload`
4. Seed via API (optional, idempotent):
   `POST /api/seed-players`
5. Run weekly pipeline:
   `POST /api/run-weekly` with body `{"week": 9, "include_crucial_actions": false}`
6. Check rankings:
   `GET /api/leaderboard`

## dashboard endpoints ##
- `GET /api/leaderboard?limit=20`
- `GET /api/weeks/{week}/snapshot`
- `GET /api/players/{player_id}/history?limit=52`
- `GET /api/job-runs?limit=20`
