# LinkedIn Bubble Analyzer

Analyze your LinkedIn feed to reveal your information bubble. This tool collects posts from your feed, measures lexical and semantic similarity, clusters posts by topic, computes a diversity score, and visualizes the results.

## How It Works

The analysis pipeline processes your LinkedIn posts through five stages:

1. **Text Cleaning** -- Strips URLs, HTML tags, normalizes whitespace, and lowercases text
2. **Lexical Similarity** -- Uses SimHash fingerprinting to detect near-duplicate posts via Hamming distance
3. **Semantic Similarity** -- Generates 384-dim sentence embeddings (all-MiniLM-L6-v2) and computes pairwise cosine similarity
4. **Topic Clustering** -- Groups posts into topics using K-Means on embeddings, with automatic cluster count selection via silhouette score. Clusters are labeled using TF-IDF top words
5. **Bubble Score** -- Computes a normalized Shannon entropy score (0 = echo chamber, 1 = diverse feed)

Visualizations include a UMAP 2D topic map, a cluster distribution pie chart, and a bubble score gauge -- all rendered as Plotly JSON.

For detailed algorithm explanations, formulas, and worked examples, see [algorithm.md](algorithm.md).

## Setup

```bash
uv venv .venv
uv sync
```

The first run will download the sentence-transformers model (~80 MB) from Hugging Face Hub.

## Running

```bash
uv run main.py
```

Visit http://127.0.0.1:8000/docs for the Swagger UI.

## Testing

```bash
# All tests (75 tests)
uv run pytest tests/ -v

# Fast tests only (skip ML model downloads)
uv run pytest tests/ -v -m "not slow"
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/posts/upload` | Upload posts (returns dataset_id) |
| GET | `/posts/{dataset_id}` | Retrieve posts by dataset |
| GET | `/posts/datasets` | List all dataset IDs |
| POST | `/analysis/run` | Run full analysis pipeline |
| GET | `/analysis/{dataset_id}` | Retrieve stored analysis |
| GET | `/visualization/{dataset_id}` | Generate Plotly visualization charts |

## Architecture

The project follows a **Layered Architecture** pattern with strict dependency rules:

```
Routes (API)  -->  Services (Business Logic)  -->  Repositories + Domain Modules  -->  Core
```

- **Routes** expose HTTP endpoints via FastAPI and validate input/output with Pydantic schemas
- **Services** orchestrate business logic by composing domain modules
- **Repositories** handle persistence through SQLAlchemy (SQLite)
- **Domain modules** implement the core algorithms (SimHash, embeddings, clustering, scoring, visualization)
- **Core** provides configuration, database setup, dependency injection, and custom exceptions

Dependencies are wired via FastAPI's `Depends()` for clean testability and separation of concerns.

### Key Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| SQLite + SQLAlchemy | Zero-config database with structured queries. Sufficient for single-user analysis workloads |
| Integer dataset IDs | Simple auto-incrementing IDs. No need for UUIDs since this is a local tool |
| Plotly JSON via API | Decouples visualization from any specific frontend. Any client can render the charts using Plotly.js |
| Lazy-loaded embedding model | The sentence-transformers model is loaded once as a singleton to avoid repeated ~80 MB model loads |
| Analysis stored as JSON | Full analysis results are serialized to a single JSON column for flexible schema evolution |
| Static service methods | Domain services (SimilarityService, ClusteringService, etc.) use static methods since they hold no state |

### Tunable Parameters

All parameters are configurable via environment variables with the `BUBBLE_` prefix:

| Variable | Default | Description |
|----------|---------|-------------|
| `BUBBLE_SIMHASH_DISTANCE_THRESHOLD` | `15` | Max Hamming distance for near-duplicate detection |
| `BUBBLE_COSINE_SIMILARITY_THRESHOLD` | `0.8` | Min cosine similarity to flag semantically similar pairs |
| `BUBBLE_DEFAULT_N_CLUSTERS` | `5` | Default K-Means cluster count (auto-detected via silhouette if not set) |
| `BUBBLE_EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformers model name |
| `BUBBLE_DATABASE_URL` | `sqlite:///./bubble_analyzer.db` | Database connection string |

### Tradeoffs

- **SimHash threshold (15)**: Lenient enough to catch paraphrased reposts, but may produce some false positives. Lower it for stricter deduplication
- **Cosine threshold (0.8)**: High bar for semantic similarity. Lower it to find more loosely related content
- **K-Means vs DBSCAN**: K-Means is predictable and fast but assumes spherical clusters. DBSCAN would auto-detect cluster count and handle noise, but is more sensitive to parameters
- **Entropy interpretation thresholds**: The 0.30/0.60 cutoffs are heuristic. Could be calibrated with empirical data from real LinkedIn feeds
- **O(N^2) pairwise comparisons**: Works well for typical feed sizes (<1000 posts). For larger datasets, approximate nearest neighbor (FAISS) would be needed

## Tech Stack

| Component | Technology |
|-----------|------------|
| Web framework | FastAPI |
| ORM / Database | SQLAlchemy + SQLite |
| Dependency management | uv |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Machine learning | scikit-learn |
| Dimensionality reduction | umap-learn |
| Visualization | Plotly |
| Validation | Pydantic + pydantic-settings |

## Project Structure

```
backend/
  routes/          # API endpoints (health, posts, analysis, visualization)
  schemas/         # Pydantic request/response models
  services/        # Business logic orchestration
  repositories/    # Data access (SQLAlchemy)
  models/          # ORM models (Post, Analysis)
  core/            # Config, database, DI, exceptions
  processing/      # Text cleaning
  similarity/      # SimHash, embeddings, cosine similarity
  clustering/      # K-Means, TF-IDF labeling
  metrics/         # Bubble diversity score
  visualization/   # UMAP projection, Plotly charts
tests/
  unit/            # Unit tests for domain modules and services
  integration/     # Integration tests for API routes + E2E pipeline
```
