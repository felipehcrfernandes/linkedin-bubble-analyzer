# LinkedIn Bubble Analyzer

Analyze your LinkedIn feed to reveal your information bubble. This tool collects posts from your feed, measures lexical and semantic similarity, clusters posts by topic, computes a diversity score, and visualizes the results.

## Setup

```bash
uv venv .venv
uv sync
```

## Running

```bash
uv run uvicorn backend.main:app --reload
```

Visit http://localhost:8000/docs for the Swagger UI.

## Testing

```bash
# All tests
uv run pytest tests/ -v

# Fast tests only (skip ML model downloads)
uv run pytest tests/ -v -m "not slow"
```

## Architecture

Layered architecture: **Routes** → **Services** → **Repositories** + **Domain Modules**

See `plan.md` for the full implementation plan.
