# Plan: "What Is Your Bubble?" — LinkedIn Feed Bubble Analyzer

## Context

This is a greenfield project to build a tool that analyzes a user's LinkedIn feed to reveal their information bubble. The tool collects posts (via a Chrome Extension), measures lexical and semantic similarity, clusters posts by topic, computes a diversity score, and visualizes the results.

**Key decisions:**
- **uv** for dependency management and virtual environment (`uv venv`, `uv add`, `uv run`)
- **TDD (Test-Driven Development)** — for every feature, write failing tests first (RED), then implement the minimum code to pass (GREEN), then refactor if needed. Tests and implementation are committed together as a single unit.
- **Layered Architecture** (routes → services → repositories → domain modules)
- **Small commits** — each task is one reviewable commit
- **SQLite + SQLAlchemy** for storage (production-ready, structured queries)
- **Plotly JSON via API** for visualization (decoupled)
- **Backend first**, Chrome Extension later

---

## TDD Workflow (applied to every feature task)

Each feature task follows this cycle within a single commit:

1. **RED**: Write the test file first with tests that define the expected behavior. Run `pytest` — tests fail (module doesn't exist yet).
2. **GREEN**: Write the minimum implementation to make all tests pass. Run `pytest` — tests pass.
3. **REFACTOR** (if needed): Clean up the implementation while keeping tests green.
4. **COMMIT**: Both test and implementation are committed together.

---

## Directory Structure

```
linkedin-bubble-analyzer/
├── .gitignore
├── CLAUDE.md
├── README.md
├── pyproject.toml
├── uv.lock
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── posts.py
│   │   ├── analysis.py
│   │   └── visualization.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── post_schemas.py
│   │   ├── analysis_schemas.py
│   │   └── visualization_schemas.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── post_service.py
│   │   ├── similarity_service.py
│   │   ├── clustering_service.py
│   │   ├── bubble_score_service.py
│   │   ├── analysis_service.py
│   │   └── visualization_service.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── post_repository.py
│   │   └── analysis_repository.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── post.py
│   │   └── analysis.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   └── dependencies.py
│   │
│   ├── processing/
│   │   ├── __init__.py
│   │   └── text_cleaner.py
│   │
│   ├── similarity/
│   │   ├── __init__.py
│   │   ├── simhash_analyzer.py
│   │   ├── embedding_generator.py
│   │   └── cosine_similarity.py
│   │
│   ├── clustering/
│   │   ├── __init__.py
│   │   ├── topic_clusterer.py
│   │   └── cluster_labeler.py
│   │
│   ├── metrics/
│   │   ├── __init__.py
│   │   └── bubble_score.py
│   │
│   └── visualization/
│       ├── __init__.py
│       ├── umap_projector.py
│       └── chart_builder.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   └── __init__.py
│   └── integration/
│       └── __init__.py
│
├── data/
│   └── sample/
│       └── sample_posts.json
│
└── scraper/
    └── chrome_extension/
        ├── manifest.json
        ├── popup.html
        ├── popup.js
        ├── content.js
        ├── background.js
        └── styles.css
```

**Layer dependency rule:** Routes → Services → Repositories + Domain Modules.

---

## Phase 0: Project Scaffolding (10 tasks)

| # | Task | Files | Commit |
|---|------|-------|--------|
| 0.0 | Create plan.md in project root | `plan.md` | `docs: add project implementation plan` |
| 0.1 | Init git repo + `.gitignore` | `.gitignore` | `chore: initialize git repository and add .gitignore` |
| 0.2 | Python project config | `pyproject.toml` | `chore: add project config and dependency files` |
| 0.3 | Backend package skeleton | `backend/**/__init__.py` (all packages) | `chore: scaffold backend package structure` |
| 0.4 | Test package skeleton + fixtures | `tests/`, `tests/conftest.py` | `chore: scaffold test directory with fixtures` |
| 0.5 | Core config + exceptions | `backend/core/config.py`, `backend/core/exceptions.py` | `feat: add core configuration and exceptions` |
| 0.6 | SQLite database setup | `backend/core/database.py`, `backend/models/base.py` | `feat: add SQLite database engine and session` |
| 0.7 | Set up uv + install deps | `uv venv .venv`, `uv add <deps>`, `uv add --dev <dev-deps>` → updates `pyproject.toml`, creates `uv.lock` | (included in 0.7 commit) |
| 0.8 | FastAPI app + health endpoint (TDD) | `tests/integration/test_health_route.py` → `backend/main.py`, `backend/routes/health.py` | `feat: create FastAPI app with health endpoint` |
| 0.9 | Sample data + README | `data/sample/sample_posts.json`, `README.md` | `docs: add sample data and README` |

**Dependency management with uv:**
```bash
uv venv .venv                  # create virtual environment
uv add <package>               # add production dependency (updates pyproject.toml + uv.lock)
uv add --dev <package>         # add dev dependency
uv run pytest                  # run commands inside the venv
uv run uvicorn backend.main:app --reload  # start dev server
```

---

## Phase 1: Data Layer — Post Ingestion & Cleaning (6 TDD tasks)

| # | Task | Test File (written FIRST) | Implementation File | Commit |
|---|------|--------------------------|-------------------|--------|
| 1.1 | Text cleaner | `tests/unit/test_text_cleaner.py` | `backend/processing/text_cleaner.py` | `feat: implement text cleaning module` |
| 1.2 | Post schemas + model | — | `backend/schemas/post_schemas.py`, `backend/models/post.py` | `feat: define post schemas and SQLAlchemy model` |
| 1.3 | Post repository | `tests/unit/test_post_repository.py` | `backend/repositories/post_repository.py` | `feat: implement post repository` |
| 1.4 | Post service | `tests/unit/test_post_service.py` | `backend/services/post_service.py` | `feat: implement post service` |
| 1.5 | Posts route + DI wiring | `tests/integration/test_posts_route.py` | `backend/routes/posts.py`, `backend/core/dependencies.py`, update `main.py` | `feat: implement posts endpoints` |
| 1.6 | Verify full data layer | Run all tests | — | (verification only) |

---

## Phase 2: Lexical Similarity — SimHash (3 TDD tasks)

| # | Task | Test File (FIRST) | Implementation File | Commit |
|---|------|-------------------|-------------------|--------|
| 2.1 | SimHash analyzer | `tests/unit/test_simhash_analyzer.py` | `backend/similarity/simhash_analyzer.py` | `feat: implement SimHash + Hamming distance` |
| 2.2 | Similarity service (lexical) | `tests/unit/test_similarity_service.py` | `backend/services/similarity_service.py` | `feat: implement lexical similarity service` |
| 2.3 | Verify lexical similarity | Run all tests | — | (verification only) |

---

## Phase 3: Semantic Similarity — Embeddings (4 TDD tasks)

| # | Task | Test File (FIRST) | Implementation File | Commit |
|---|------|-------------------|-------------------|--------|
| 3.1 | Embedding generator | `tests/unit/test_embedding_generator.py` | `backend/similarity/embedding_generator.py` | `feat: implement embedding generator` |
| 3.2 | Cosine similarity | `tests/unit/test_cosine_similarity.py` | `backend/similarity/cosine_similarity.py` | `feat: implement cosine similarity` |
| 3.3 | Extend similarity service | update `tests/unit/test_similarity_service.py` | update `backend/services/similarity_service.py` | `feat: add semantic analysis to similarity service` |
| 3.4 | Verify semantic similarity | Run all tests | — | (verification only) |

---

## Phase 4: Topic Clustering — K-Means (3 TDD tasks)

| # | Task | Test File (FIRST) | Implementation File | Commit |
|---|------|-------------------|-------------------|--------|
| 4.1 | Topic clusterer | `tests/unit/test_topic_clusterer.py` | `backend/clustering/topic_clusterer.py` | `feat: implement K-Means clustering` |
| 4.2 | Cluster labeler | `tests/unit/test_cluster_labeler.py` | `backend/clustering/cluster_labeler.py` | `feat: implement TF-IDF cluster labeling` |
| 4.3 | Clustering service | `tests/unit/test_clustering_service.py` | `backend/services/clustering_service.py` | `feat: implement clustering service` |

---

## Phase 5: Bubble Diversity Score (2 TDD tasks)

| # | Task | Test File (FIRST) | Implementation File | Commit |
|---|------|-------------------|-------------------|--------|
| 5.1 | Bubble score module | `tests/unit/test_bubble_score.py` | `backend/metrics/bubble_score.py` | `feat: implement bubble diversity score` |
| 5.2 | Bubble score service | `tests/unit/test_bubble_score_service.py` | `backend/services/bubble_score_service.py` | `feat: implement bubble score service` |

---

## Phase 6: Visualization — UMAP + Plotly (3 TDD tasks)

| # | Task | Test File (FIRST) | Implementation File | Commit |
|---|------|-------------------|-------------------|--------|
| 6.1 | UMAP projector | `tests/unit/test_umap_projector.py` | `backend/visualization/umap_projector.py` | `feat: implement UMAP 2D projection` |
| 6.2 | Plotly chart builder | `tests/unit/test_chart_builder.py` | `backend/visualization/chart_builder.py` | `feat: implement Plotly chart builders` |
| 6.3 | Visualization service | `tests/unit/test_visualization_service.py` | `backend/services/visualization_service.py` | `feat: implement visualization service` |

---

## Phase 7: Full Pipeline + API Endpoints (7 TDD tasks)

| # | Task | Test File (FIRST) | Implementation File | Commit |
|---|------|-------------------|-------------------|--------|
| 7.1 | Analysis + viz schemas | — | `backend/schemas/analysis_schemas.py`, `backend/schemas/visualization_schemas.py` | `feat: define analysis and visualization schemas` |
| 7.2 | Analysis model + repository | `tests/unit/test_analysis_repository.py` | `backend/models/analysis.py`, `backend/repositories/analysis_repository.py` | `feat: implement analysis repository` |
| 7.3 | Analysis service | `tests/unit/test_analysis_service.py` | `backend/services/analysis_service.py` | `feat: implement analysis pipeline service` |
| 7.4 | Wire all DI + analysis route | `tests/integration/test_analysis_route.py` | `backend/core/dependencies.py`, `backend/routes/analysis.py`, update `main.py` | `feat: implement analysis endpoints` |
| 7.5 | Visualization route | `tests/integration/test_visualization_route.py` | `backend/routes/visualization.py`, update `main.py` | `feat: implement visualization endpoints` |
| 7.6 | End-to-end pipeline test | `tests/integration/test_analysis_pipeline.py` | — | `test: add end-to-end pipeline test` |
| 7.7 | Verify full backend | Run all tests | — | (verification only) |

---

## Phase 8: Chrome Extension (7 tasks)

| # | Task | Files | Commit |
|---|------|-------|--------|
| 8.1 | Manifest V3 | `scraper/chrome_extension/manifest.json` | `feat: create Chrome Extension manifest` |
| 8.2 | Content script | `content.js` | `feat: implement LinkedIn feed scraping` |
| 8.3 | Popup UI | `popup.html`, `popup.js`, `styles.css` | `feat: implement extension popup UI` |
| 8.4 | Background service worker | `background.js` | `feat: implement background service worker` |
| 8.5 | JSON export | update `popup.js`, `background.js` | `feat: add JSON export` |
| 8.6 | Backend integration | update `popup.js`, `background.js` | `feat: integrate extension with backend API` |
| 8.7 | Icons + polish | `icons/` | `feat: add extension icons and finalize` |

---

## Phase 9: Polish & Hardening (4 tasks)

| # | Task | Files | Commit |
|---|------|-------|--------|
| 9.1 | Structured logging | services + `main.py` | `feat: add structured logging` |
| 9.2 | Global exception handlers | `backend/main.py` | `feat: add global exception handlers` |
| 9.3 | CORS config for extension | `config.py`, `main.py` | `feat: configure CORS for Chrome Extension` |
| 9.4 | Final README | `README.md` | `docs: final README with full documentation` |

---

## Summary

| Phase | Focus | Tasks |
|-------|-------|-------|
| 0 | Scaffolding | 10 |
| 1 | Post ingestion + cleaning (TDD) | 6 |
| 2 | Lexical similarity (TDD) | 3 |
| 3 | Semantic similarity (TDD) | 4 |
| 4 | Topic clustering (TDD) | 3 |
| 5 | Bubble diversity score (TDD) | 2 |
| 6 | Visualization (TDD) | 3 |
| 7 | Full pipeline + API (TDD) | 7 |
| 8 | Chrome Extension | 7 |
| 9 | Polish + docs | 4 |
| **Total** | | **49** |
