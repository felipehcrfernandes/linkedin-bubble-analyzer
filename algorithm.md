# LinkedIn Bubble Analyzer -- Algorithms and Architecture

This document provides a detailed technical reference for every algorithm and
architectural decision in the LinkedIn Bubble Analyzer. It is written for
anyone who wants to study the techniques, reproduce the results, or extend the
system.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [Pipeline Flow](#3-pipeline-flow)
4. [Text Preprocessing](#4-text-preprocessing)
5. [Lexical Similarity -- SimHash](#5-lexical-similarity--simhash)
6. [Semantic Similarity -- Sentence Embeddings and Cosine Similarity](#6-semantic-similarity--sentence-embeddings-and-cosine-similarity)
7. [Topic Clustering -- K-Means](#7-topic-clustering--k-means)
8. [Cluster Labeling -- TF-IDF](#8-cluster-labeling--tf-idf)
9. [Bubble Diversity Score -- Normalized Shannon Entropy](#9-bubble-diversity-score--normalized-shannon-entropy)
10. [Visualization -- UMAP and Plotly](#10-visualization--umap-and-plotly)
11. [Tunable Parameters](#11-tunable-parameters)
12. [Tradeoffs and Future Directions](#12-tradeoffs-and-future-directions)

---

## 1. Project Overview

The LinkedIn Bubble Analyzer is a tool that takes a collection of posts from a
user's LinkedIn feed, measures how similar and clustered they are, and produces
a numerical "bubble score" that quantifies how diverse or narrow the user's
information environment is.

The end-to-end pipeline:

```
Upload posts --> Clean text --> Generate embeddings --> Compute SimHash
    --> Cluster by topic --> Label clusters --> Score diversity --> Visualize
```

Key questions the tool answers:

- **Are there near-duplicate posts in the feed?** (SimHash)
- **How semantically similar are the posts?** (Cosine similarity on embeddings)
- **What topics dominate the feed?** (K-Means clustering + TF-IDF labels)
- **How diverse is the feed overall?** (Normalized Shannon entropy)
- **What does this look like visually?** (UMAP 2D projection + Plotly charts)

---

## 2. Architecture

### 2.1 Layered Architecture

The project follows a **Layered Architecture** pattern, which separates concerns
into distinct horizontal layers. Each layer only depends on the layer below it.

```
 +-------------------------------------------------+
 |                   Routes (API)                   |
 |   backend/routes/posts.py                        |
 |   backend/routes/health.py                       |
 +-------------------------------------------------+
                        |
                        v
 +-------------------------------------------------+
 |                   Services                       |
 |   backend/services/analysis_service.py           |
 |   backend/services/post_service.py               |
 |   backend/services/similarity_service.py         |
 |   backend/services/clustering_service.py         |
 |   backend/services/bubble_score_service.py       |
 |   backend/services/visualization_service.py      |
 +-------------------------------------------------+
                        |
                        v
 +-------------------------------------------------+
 |         Repositories + Domain Modules            |
 |   backend/repositories/post_repository.py        |
 |   backend/repositories/analysis_repository.py    |
 |   backend/processing/text_cleaner.py             |
 |   backend/similarity/simhash_analyzer.py         |
 |   backend/similarity/embedding_generator.py      |
 |   backend/similarity/cosine_similarity.py        |
 |   backend/clustering/topic_clusterer.py          |
 |   backend/clustering/cluster_labeler.py          |
 |   backend/metrics/bubble_score.py                |
 |   backend/visualization/umap_projector.py        |
 |   backend/visualization/chart_builder.py         |
 +-------------------------------------------------+
                        |
                        v
 +-------------------------------------------------+
 |               Core / Infrastructure              |
 |   backend/core/config.py                         |
 |   backend/core/database.py                       |
 |   backend/core/dependencies.py                   |
 |   backend/core/exceptions.py                     |
 |   backend/models/post.py                         |
 |   backend/models/analysis.py                     |
 +-------------------------------------------------+
```

**Routes** expose HTTP endpoints via FastAPI and delegate work to services.
**Services** orchestrate business logic by calling domain modules and
repositories. **Repositories** handle persistence through SQLAlchemy.
**Domain modules** implement the core algorithms (SimHash, embeddings,
clustering, scoring, visualization). **Core** holds configuration, database
setup, and dependency injection.

### 2.2 Tech Stack

| Component              | Technology                  |
|------------------------|-----------------------------|
| Web framework          | FastAPI                     |
| ORM / Database         | SQLAlchemy + SQLite         |
| Dependency management  | uv                          |
| Embeddings             | sentence-transformers       |
| Machine learning       | scikit-learn                |
| Dimensionality reduction | umap-learn                |
| Visualization          | Plotly                      |
| Validation             | Pydantic + pydantic-settings |

### 2.3 Data Models

Two SQLAlchemy models back the persistence layer:

**Post** (`backend/models/post.py`):

| Column        | Type    | Notes                         |
|---------------|---------|-------------------------------|
| id            | Integer | Primary key, auto-increment   |
| dataset_id    | Integer | Groups posts by upload batch  |
| author        | String  | Post author                   |
| content       | Text    | Original post content         |
| cleaned_text  | Text    | Preprocessed text (nullable)  |
| date          | String  | Post date (nullable)          |

**Analysis** (`backend/models/analysis.py`):

| Column       | Type    | Notes                                  |
|--------------|---------|----------------------------------------|
| id           | Integer | Primary key, auto-increment            |
| dataset_id   | Integer | Unique, references the upload batch    |
| result_json  | Text    | Full analysis result serialized as JSON|

---

## 3. Pipeline Flow

When a user triggers an analysis, the `AnalysisService.run_analysis` method
orchestrates the complete pipeline:

```
                    +----------------+
                    |  Upload Posts   |
                    | (POST /posts)  |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    |  Clean Text    |
                    | text_cleaner   |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    | Store in DB    |
                    | PostRepository |
                    +-------+--------+
                            |
                            v
                  +---------+---------+
                  |                   |
                  v                   v
        +-----------------+  +-----------------+
        | SimHash         |  | Embeddings      |
        | (Lexical)       |  | (Semantic)      |
        +--------+--------+  +--------+--------+
                 |                     |
                 v                     v
        +-----------------+  +-----------------+
        | Near-Duplicate  |  | Cosine Sim      |
        | Detection       |  | Matrix + Pairs  |
        +-----------------+  +--------+--------+
                                       |
                                       v
                              +-----------------+
                              | K-Means         |
                              | Clustering      |
                              +--------+--------+
                                       |
                                       v
                              +-----------------+
                              | TF-IDF          |
                              | Cluster Labels  |
                              +--------+--------+
                                       |
                                       v
                              +-----------------+
                              | Shannon Entropy |
                              | Bubble Score    |
                              +--------+--------+
                                       |
                                       v
                              +-----------------+
                              | UMAP + Plotly   |
                              | Visualization   |
                              +-----------------+
```

In code (`backend/services/analysis_service.py`):

```python
def run_analysis(self, dataset_id: int, n_clusters: int | None = None) -> dict:
    posts = self.post_service.get_posts(dataset_id)
    texts = [p["cleaned_text"] for p in posts]

    lexical = SimilarityService.compute_lexical_similarity(texts)
    semantic = SimilarityService.compute_semantic_similarity(texts)
    clustering = ClusteringService.cluster_and_label(
        texts, semantic["embeddings"], n_clusters=n_clusters
    )
    bubble = BubbleScoreService.compute(clustering["distribution"])
    # ... assemble and persist result
```

---

## 4. Text Preprocessing

**File:** `backend/processing/text_cleaner.py`

Before any analysis, raw post text must be cleaned. The preprocessing pipeline
applies four transformations in sequence:

### 4.1 Steps

1. **URL removal** -- Strip all HTTP(S) URLs.
   ```
   regex: https?://\S+
   ```
   LinkedIn posts often contain links that add noise to text similarity
   comparisons without carrying topical meaning.

2. **HTML tag stripping** -- Remove any HTML markup.
   ```
   regex: <[^>]+>
   ```
   Some post exports include raw HTML. Tags like `<br>`, `<b>`, etc. are
   irrelevant to the semantic content.

3. **Lowercasing** -- Convert the entire string to lowercase.
   This ensures "Machine Learning" and "machine learning" are treated
   identically for similarity and clustering.

4. **Whitespace normalization** -- Collapse all consecutive whitespace
   (spaces, tabs, newlines) into a single space and strip leading/trailing
   whitespace.
   ```
   regex: \s+  -->  " "
   ```

### 4.2 Implementation

```python
def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"https?://\S+", "", text)   # Step 1
    text = re.sub(r"<[^>]+>", "", text)         # Step 2
    text = text.lower()                          # Step 3
    text = re.sub(r"\s+", " ", text).strip()    # Step 4
    return text
```

The `clean_post` wrapper function takes a raw post dictionary, applies
`clean_text` to its `content` field, and stores the result under the key
`cleaned_text`.

### 4.3 Why These Steps Matter

Skipping URL removal would cause posts sharing the same link to appear more
similar than they semantically are. Skipping lowercasing would split the
embedding space unnecessarily. Whitespace normalization prevents tokenization
artifacts in downstream algorithms (SimHash shingles, TF-IDF tokens).

---

## 5. Lexical Similarity -- SimHash

**File:** `backend/similarity/simhash_analyzer.py`

SimHash is a locality-sensitive hashing technique originally developed by Moses
Charikar (2002) and popularized by Google for web-page deduplication. It
provides a fast, constant-space way to detect near-duplicate texts.

### 5.1 How SimHash Works

The algorithm converts a text document into a single 64-bit fingerprint such
that similar documents produce similar fingerprints.

**Step-by-step process:**

1. **Shingling (tokenization):** Split the input text into tokens (typically
   word-level unigrams or character n-grams). The `simhash` Python library
   uses word-level tokens by default.

2. **Hashing each token:** Apply a standard hash function (e.g., MD5, FNV) to
   each token, producing a 64-bit hash for every token.

3. **Weighted bit vector:** Initialize a vector `V` of 64 zeros. For each
   token hash:
   - For each bit position `i` (0 through 63):
     - If bit `i` is 1, add +1 to `V[i]`
     - If bit `i` is 0, add -1 to `V[i]`
   - Tokens can optionally carry weights (e.g., TF-IDF weight), which scale
     the +1/-1 contribution.

4. **Collapse to fingerprint:** Convert `V` into a 64-bit fingerprint:
   - For each position `i`: if `V[i] > 0`, set bit `i` to 1; otherwise 0.

```
Example (simplified to 8 bits):

Tokens: ["machine", "learning", "python"]

Hash("machine")  = 10110100
Hash("learning") = 11001010
Hash("python")   = 10100110

Weighted vector V:
  bit 0: +1 -1 +1 = +1  --> 1
  bit 1: -1 +1 -1 = -1  --> 0
  bit 2: +1 -1 +1 = +1  --> 1
  bit 3: +1 -1 -1 = -1  --> 0
  bit 4: -1 +1 -1 = -1  --> 0
  bit 5: +1 -1 +1 = +1  --> 1
  bit 6: -1 +1 +1 = +1  --> 1
  bit 7: -1 -1 -1 = -1  --> 0

Fingerprint: 10100110
```

### 5.2 Hamming Distance

The **Hamming distance** between two SimHash fingerprints is the number of bit
positions where they differ. It is computed efficiently using XOR followed by
a popcount (count of set bits):

```
hamming(h1, h2) = popcount(h1 XOR h2)
```

For 64-bit hashes, the Hamming distance ranges from 0 (identical) to 64
(completely different).

**Interpretation:**
- Distance 0: The texts are (very likely) identical.
- Distance <= threshold: The texts are near-duplicates.
- Distance > threshold: The texts are sufficiently different.

### 5.3 Implementation Details

```python
from simhash import Simhash

def compute_simhash(text: str) -> Simhash:
    return Simhash(text)

def hamming_distance(h1: Simhash, h2: Simhash) -> int:
    return h1.distance(h2)
```

The `compute_simhash_matrix` function builds a full N x N pairwise distance
matrix for all texts. The `find_near_duplicates` function returns only those
pairs whose distance falls at or below a given threshold.

### 5.4 Threshold

Default: **15** (configurable via `BUBBLE_SIMHASH_DISTANCE_THRESHOLD`).

With 64 bits, a threshold of 15 means roughly 23% of bits can differ and the
texts are still considered near-duplicates. This is a relatively lenient
threshold suited for detecting paraphrased or lightly edited reposts on
LinkedIn.

### 5.5 Computational Complexity

- Computing SimHash for one text: O(n) where n is the number of tokens.
- Comparing all pairs: O(N^2) where N is the number of posts.
- Each comparison: O(1) (XOR + popcount on 64-bit integers).

SimHash is particularly efficient because it reduces the full text to a
fixed-size fingerprint, making storage and comparison trivially fast.

### 5.6 Why SimHash Instead of Other Approaches

| Alternative       | Drawback compared to SimHash                      |
|-------------------|----------------------------------------------------|
| Exact hash (MD5)  | Only detects identical texts, not near-duplicates  |
| MinHash + LSH     | Better for set similarity (Jaccard), more complex  |
| Edit distance     | O(n^2) per pair, too slow for large feeds          |

SimHash is ideal for a quick lexical pass before the more expensive semantic
analysis.

---

## 6. Semantic Similarity -- Sentence Embeddings and Cosine Similarity

### 6.1 Sentence Embeddings

**File:** `backend/similarity/embedding_generator.py`

The system uses the **`all-MiniLM-L6-v2`** model from the
[sentence-transformers](https://www.sbert.net/) library to convert each
cleaned post into a dense numerical vector (embedding).

#### About the Model

| Property         | Value                        |
|------------------|------------------------------|
| Name             | all-MiniLM-L6-v2             |
| Architecture     | MiniLM (distilled BERT)      |
| Layers           | 6 transformer layers         |
| Embedding dim    | 384                          |
| Model size       | ~80 MB                       |
| Max sequence len | 256 word pieces              |
| Training data    | 1B+ sentence pairs           |

**Why this model:**

- **Small and fast:** At ~80 MB and 6 layers, it loads quickly and runs
  inference on CPU in reasonable time. This matters for a tool that will be
  deployed on a developer's machine, not a GPU cluster.
- **Good quality for short texts:** LinkedIn posts are typically short
  (a few sentences to a few paragraphs). The model was trained specifically
  for sentence-level similarity tasks and performs well on benchmarks like
  STS (Semantic Textual Similarity).
- **Widely adopted:** The model is well-documented, stable, and available on
  Hugging Face Hub.

#### How Sentence Embeddings Work (Conceptual)

1. Tokenize the input text into subword tokens (WordPiece).
2. Pass tokens through 6 transformer layers with self-attention.
3. Pool the final-layer hidden states (mean pooling over all tokens).
4. The result is a 384-dimensional vector that captures semantic meaning.

Texts with similar meaning will have vectors that point in similar directions
in this 384-dimensional space, even if they use completely different words.

#### Implementation

```python
class EmbeddingGenerator:
    def __init__(self, model_name: str | None = None):
        self.model = SentenceTransformer(model_name or settings.embedding_model)

    def generate(self, texts: list[str]) -> np.ndarray:
        return self.model.encode(texts, convert_to_numpy=True)
```

The `EmbeddingGenerator` is instantiated as a module-level singleton in
`SimilarityService` to avoid reloading the model on every request.

### 6.2 Cosine Similarity

**File:** `backend/similarity/cosine_similarity.py`

Once we have embedding vectors, we measure how similar two texts are by
computing the **cosine similarity** between their vectors.

#### Mathematical Definition

For two vectors **A** and **B**:

```
                  A . B           sum(A_i * B_i)
cos(A, B) = ------------- = ---------------------------
             ||A|| ||B||    sqrt(sum(A_i^2)) * sqrt(sum(B_i^2))
```

Where:
- `A . B` is the dot product
- `||A||` and `||B||` are the L2 norms (Euclidean lengths)

**Range:** [-1, 1] for general vectors, but [0, 1] for sentence embeddings
(since the model produces non-negative-dominant vectors).

**Interpretation:**
- 1.0 = identical meaning (vectors point in the same direction)
- 0.0 = completely unrelated (vectors are orthogonal)
- Close to 1.0 = very similar meaning

#### Why Cosine Similarity?

Cosine similarity measures the **angle** between vectors, not their magnitude.
This is important because:

- Two posts about the same topic but of different lengths will have vectors
  of different magnitudes but similar directions.
- We care about **what** the text says, not **how much** it says.

Alternative: Euclidean distance measures magnitude differences too, which would
penalize longer texts unfairly.

#### Implementation

```python
def cosine_similarity_matrix(vectors: np.ndarray) -> np.ndarray:
    return sklearn_cosine(vectors)  # scikit-learn's optimized implementation

def find_similar_pairs(vectors: np.ndarray, threshold: float = 0.8) -> list[dict]:
    matrix = cosine_similarity_matrix(vectors)
    n = matrix.shape[0]
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] >= threshold:
                pairs.append({"i": i, "j": j, "similarity": float(matrix[i][j])})
    return pairs
```

The `average_similarity` function computes the mean of all pairwise
similarities (excluding self-similarity on the diagonal). A high average
similarity indicates the feed is dominated by a narrow set of topics.

#### Threshold

Default: **0.8** (configurable via `BUBBLE_COSINE_SIMILARITY_THRESHOLD`).

A cosine similarity of 0.8 is quite high -- it indicates the two posts are
very close in meaning. This threshold focuses on identifying truly similar
content, not loosely related posts.

---

## 7. Topic Clustering -- K-Means

**File:** `backend/clustering/topic_clusterer.py`

K-Means clustering groups the embedding vectors into `k` clusters, where each
cluster represents a topic in the feed.

### 7.1 How K-Means Works

K-Means is an iterative algorithm that partitions N data points into k
non-overlapping clusters by minimizing within-cluster variance.

**Algorithm:**

```
1. Initialize k centroids (randomly or via k-means++).
2. Repeat until convergence:
   a. ASSIGN: For each data point, find the nearest centroid.
      Assign the point to that centroid's cluster.
   b. UPDATE: Recompute each centroid as the mean of all
      points assigned to its cluster.
3. Convergence: Stop when assignments no longer change
   (or after max iterations).
```

**Objective function (inertia):**

```
J = sum over k clusters of (sum over points x in cluster_k of ||x - mu_k||^2)
```

Where `mu_k` is the centroid (mean vector) of cluster k.

### 7.2 Implementation

```python
class TopicClusterer:
    @staticmethod
    def cluster(embeddings: np.ndarray, n_clusters: int = 5):
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings).tolist()
        distribution = {}
        total = len(labels)
        for cluster_id in range(n_clusters):
            count = labels.count(cluster_id)
            distribution[cluster_id] = count / total
        return labels, distribution
```

Key parameters:
- `random_state=42`: Ensures reproducible results across runs.
- `n_init=10`: Runs the algorithm 10 times with different initial centroids
  and keeps the best result (lowest inertia). This mitigates the sensitivity
  of K-Means to initialization.

The method returns:
- `labels`: A list mapping each post to its cluster ID (0 through k-1).
- `distribution`: A dictionary mapping each cluster ID to the proportion of
  posts it contains (e.g., `{0: 0.40, 1: 0.35, 2: 0.25}`).

### 7.3 Optimal k Selection via Silhouette Score

When the user does not specify the number of clusters, the system automatically
finds the best `k` using the **silhouette score**.

**Silhouette score** for a single data point `i`:

```
         b(i) - a(i)
s(i) = ---------------
        max(a(i), b(i))
```

Where:
- `a(i)` = mean distance from point `i` to all other points **in the same
  cluster** (intra-cluster distance, measures cohesion).
- `b(i)` = mean distance from point `i` to all points **in the nearest
  neighboring cluster** (inter-cluster distance, measures separation).

**Range:** [-1, 1]
- +1 = the point is well inside its own cluster, far from others.
- 0 = the point is on the boundary between two clusters.
- -1 = the point is likely assigned to the wrong cluster.

The **overall silhouette score** is the mean of `s(i)` across all data points.

```python
@staticmethod
def find_optimal_k(embeddings: np.ndarray, k_range: tuple[int, int] = (2, 8)):
    best_k = k_range[0]
    best_score = -1.0
    for k in range(k_range[0], k_range[1] + 1):
        if k >= len(embeddings):
            break
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings)
        score = silhouette_score(embeddings, labels)
        if score > best_score:
            best_score = score
            best_k = k
    return best_k
```

The system tests every k from 2 to min(8, N-1), clusters the data with each k,
computes the silhouette score, and returns the k that maximizes it.

### 7.4 Why K-Means?

| Alternative  | Pros                          | Cons                                |
|--------------|-------------------------------|-------------------------------------|
| K-Means      | Simple, predictable, fast     | Must pre-specify k                  |
| DBSCAN       | Automatic k, finds noise      | Sensitive to epsilon, less predictable |
| Agglomerative| Hierarchical, no k needed     | Slower, O(N^2) memory              |
| Gaussian Mixture | Soft assignments           | More complex, overfitting risk      |

K-Means was chosen because:
- It is **predictable** -- given the same data and k, it always produces the
  same result (with fixed random state).
- It is **fast** -- O(N * k * d * iterations), where d=384.
- Combined with silhouette analysis, the k selection is automatic yet stable.

---

## 8. Cluster Labeling -- TF-IDF

**File:** `backend/clustering/cluster_labeler.py`

After K-Means assigns each post to a cluster, we need human-readable labels
for the clusters. TF-IDF (Term Frequency - Inverse Document Frequency) extracts
the most distinctive words per cluster.

### 8.1 How TF-IDF Works

TF-IDF is a numerical statistic that reflects how important a word is to a
document within a corpus.

**Term Frequency (TF):**

```
TF(t, d) = (number of times term t appears in document d)
            / (total number of terms in document d)
```

**Inverse Document Frequency (IDF):**

```
IDF(t, D) = log( (total number of documents in D)
                 / (number of documents containing term t) )
```

**TF-IDF score:**

```
TF-IDF(t, d, D) = TF(t, d) * IDF(t, D)
```

**Intuition:**
- A word that appears frequently in one cluster document but rarely in others
  gets a high TF-IDF score. This word is **distinctive** to that cluster.
- A word that appears everywhere (like "the", "is") gets a low IDF, driving
  its TF-IDF score down.

### 8.2 Application to Cluster Labeling

The implementation treats each cluster as a single "document" by concatenating
all post texts belonging to that cluster:

```python
@staticmethod
def label_clusters(texts, labels, top_n=5):
    cluster_ids = sorted(set(labels))
    cluster_texts = {}
    for cluster_id in cluster_ids:
        cluster_texts[cluster_id] = " ".join(
            text for text, label in zip(texts, labels) if label == cluster_id
        )

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(cluster_texts.values())
    feature_names = vectorizer.get_feature_names_out()

    result = {}
    for idx, cluster_id in enumerate(cluster_ids):
        scores = tfidf_matrix[idx].toarray().flatten()
        top_indices = scores.argsort()[-top_n:][::-1]
        result[cluster_id] = [feature_names[i] for i in top_indices]
    return result
```

**Process:**
1. Concatenate all texts in each cluster into one "mega-document."
2. Fit a `TfidfVectorizer` across all cluster documents (with English stop
   word removal).
3. For each cluster document, extract the top `top_n` (default: 5) words with
   the highest TF-IDF scores.
4. These words serve as the cluster's thematic label.

**Stop words:** The `stop_words="english"` parameter removes common English
function words (the, is, at, which, on, ...) that carry no topical meaning.

### 8.3 Cluster Summary

The `format_cluster_summary` method assembles a list of dictionaries, one per
cluster, containing:

| Field        | Description                                        |
|--------------|----------------------------------------------------|
| cluster_id   | Integer cluster identifier (0-indexed)              |
| proportion   | Fraction of all posts in this cluster (0.0 to 1.0) |
| top_words    | List of the top TF-IDF words for this cluster      |
| post_count   | Absolute number of posts in the cluster            |

---

## 9. Bubble Diversity Score -- Normalized Shannon Entropy

**File:** `backend/metrics/bubble_score.py`

The bubble score quantifies how evenly distributed the user's feed is across
topics. It uses **normalized Shannon entropy** -- a concept from information
theory.

### 9.1 Shannon Entropy

Shannon entropy measures the uncertainty (or diversity) of a probability
distribution. Given a set of clusters with proportions `p_1, p_2, ..., p_k`:

```
H = - sum from i=1 to k of ( p_i * log2(p_i) )
```

Where `p_i` is the proportion of posts in cluster `i` (i.e.,
`count_in_cluster_i / total_posts`).

**Properties:**
- **Minimum (H = 0):** All posts are in a single cluster. There is no
  uncertainty -- the feed is a pure echo chamber.
- **Maximum (H = log2(k)):** Posts are perfectly uniformly distributed across
  all k clusters. Maximum diversity.

### 9.2 Normalization

To make the score comparable across different values of k, we normalize by
dividing by the maximum possible entropy:

```
Bubble Score = H / H_max = H / log2(k)
```

This yields a score in the range [0, 1] regardless of how many clusters exist.

### 9.3 Implementation

```python
def compute_bubble_score(distribution: dict[int, float]) -> float:
    n = len(distribution)
    if n <= 1:
        return 0.0
    entropy = -sum(p * math.log2(p) for p in distribution.values() if p > 0)
    max_entropy = math.log2(n)
    return entropy / max_entropy
```

Note: The `if p > 0` guard prevents `log2(0)` which is undefined.

### 9.4 Interpretation Thresholds

```python
def interpret_score(score: float) -> str:
    if score < 0.30:
        return "strong bubble"
    elif score < 0.60:
        return "moderate bubble"
    else:
        return "diverse feed"
```

| Score Range | Interpretation   | What It Means                                  |
|-------------|------------------|------------------------------------------------|
| 0.00 - 0.29 | Strong bubble   | Feed is heavily concentrated in one or two topics. The user is in a deep information silo. |
| 0.30 - 0.59 | Moderate bubble | Some topical diversity exists, but certain topics dominate significantly. |
| 0.60 - 1.00 | Diverse feed    | Posts are spread reasonably evenly across multiple topics. The user is exposed to varied content. |

### 9.5 Worked Example

Suppose k = 4 clusters with the following distribution:

```
Cluster 0: 50 posts (50%)  p_0 = 0.50
Cluster 1: 30 posts (30%)  p_1 = 0.30
Cluster 2: 15 posts (15%)  p_2 = 0.15
Cluster 3:  5 posts  (5%)  p_3 = 0.05
```

**Shannon entropy:**

```
H = -(0.50 * log2(0.50) + 0.30 * log2(0.30) + 0.15 * log2(0.15) + 0.05 * log2(0.05))
H = -(0.50 * (-1.0) + 0.30 * (-1.737) + 0.15 * (-2.737) + 0.05 * (-4.322))
H = -(-0.500 + (-0.521) + (-0.411) + (-0.216))
H = -(-1.648)
H = 1.648 bits
```

**Maximum entropy:**

```
H_max = log2(4) = 2.0 bits
```

**Bubble score:**

```
Score = 1.648 / 2.0 = 0.824
```

Interpretation: **diverse feed** (> 0.60). Even though cluster 0 has half the
posts, the overall distribution is diverse enough.

---

## 10. Visualization -- UMAP and Plotly

### 10.1 UMAP Dimensionality Reduction

**File:** `backend/visualization/umap_projector.py`

UMAP (Uniform Manifold Approximation and Projection) reduces the
384-dimensional embedding vectors to 2 dimensions for scatter plot
visualization.

#### How UMAP Works (Conceptual)

1. **Build a high-dimensional graph:** For each point, find its k nearest
   neighbors. Construct a weighted graph where edge weights reflect the
   probability that two points are connected (using a local fuzzy simplicial
   set).

2. **Optimize a low-dimensional layout:** Initialize points in 2D and
   iteratively move them so that the 2D distance structure matches the
   high-dimensional graph structure as closely as possible. This is done by
   minimizing a cross-entropy loss between the high-dimensional and
   low-dimensional edge probabilities.

#### Why UMAP Over t-SNE?

| Property                 | UMAP           | t-SNE           |
|--------------------------|----------------|-----------------|
| Global structure         | Preserved      | Often lost      |
| Speed                    | Faster         | Slower          |
| Determinism              | With seed, yes | Less stable     |
| Parameter sensitivity    | Moderate       | High            |

UMAP tends to produce more meaningful cluster separation in the 2D projection
while keeping the relative distances between clusters intact. t-SNE focuses
heavily on local neighborhoods and can distort global relationships.

#### Implementation

```python
class UmapProjector:
    @staticmethod
    def project(embeddings: np.ndarray) -> np.ndarray:
        n_neighbors = min(15, len(embeddings) - 1)
        reducer = umap.UMAP(n_components=2, random_state=42, n_neighbors=n_neighbors)
        return reducer.fit_transform(embeddings)
```

Key parameters:
- `n_components=2`: Project down to 2 dimensions for plotting.
- `random_state=42`: Reproducible projections.
- `n_neighbors=min(15, N-1)`: Controls the balance between local and global
  structure. Lower values preserve more local detail; higher values preserve
  more global structure. The default of 15 is standard. The `min` guard
  ensures it does not exceed the number of available data points.

The `project_with_metadata` method enriches each projected point with its
cluster label and original text for hover tooltips.

### 10.2 Plotly Charts

**File:** `backend/visualization/chart_builder.py`

Three interactive charts are generated as JSON (Plotly JSON format):

#### Chart 1: Topic Map (Scatter Plot)

A 2D scatter plot of the UMAP-projected embeddings, colored by cluster ID.
Each point represents a post. Hovering shows the post text.

```python
fig.add_trace(go.Scatter(
    x=[p["x"] for p in cluster_points],
    y=[p["y"] for p in cluster_points],
    mode="markers",
    name=f"Cluster {cluster_id}",
    text=[p["text"] for p in cluster_points],
    hovertemplate="%{text}<extra></extra>",
))
```

This visualization directly shows:
- How tightly grouped the clusters are (tight = strong topic coherence).
- Whether clusters overlap (overlap = ambiguous topic boundaries).
- Outlier posts that do not fit any cluster well.

#### Chart 2: Distribution (Pie Chart)

Shows the proportion of posts in each cluster. Labels include the top 3 TF-IDF
words for context.

```python
labels = [f"Cluster {s['cluster_id']}: {', '.join(s['top_words'][:3])}" ...]
values = [s["proportion"] for s in cluster_summary]
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
```

A highly skewed pie chart visually confirms a bubble.

#### Chart 3: Bubble Indicator (Gauge)

A gauge chart showing the bubble score from 0 to 1 with three color-coded
zones:

```
 Red    (0.0 - 0.3): strong bubble
 Yellow (0.3 - 0.6): moderate bubble
 Green  (0.6 - 1.0): diverse feed
```

```python
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=score,
    gauge={
        "axis": {"range": [0, 1]},
        "steps": [
            {"range": [0, 0.3], "color": "red"},
            {"range": [0.3, 0.6], "color": "yellow"},
            {"range": [0.6, 1.0], "color": "green"},
        ],
    },
))
```

All charts are serialized to JSON via `fig.to_json()` so that a frontend can
render them directly with Plotly.js.

---

## 11. Tunable Parameters

All parameters are configured via environment variables with the prefix
`BUBBLE_` and managed by Pydantic Settings in `backend/core/config.py`.

| Environment Variable                    | Setting Name                   | Default            | Description                                                |
|-----------------------------------------|--------------------------------|--------------------|------------------------------------------------------------|
| `BUBBLE_SIMHASH_DISTANCE_THRESHOLD`     | `simhash_distance_threshold`   | `15`               | Max Hamming distance to consider two posts near-duplicates. Lower = stricter. |
| `BUBBLE_COSINE_SIMILARITY_THRESHOLD`    | `cosine_similarity_threshold`  | `0.8`              | Min cosine similarity to consider two posts semantically similar. Lower = more pairs found. |
| `BUBBLE_DEFAULT_N_CLUSTERS`             | `default_n_clusters`           | `5`                | Default number of K-Means clusters when not auto-detected. |
| `BUBBLE_EMBEDDING_MODEL`               | `embedding_model`              | `all-MiniLM-L6-v2` | Sentence-transformers model for generating embeddings.     |
| `BUBBLE_DATABASE_URL`                   | `database_url`                 | `sqlite:///./bubble_analyzer.db` | SQLAlchemy database connection string.       |
| `BUBBLE_DEBUG`                          | `debug`                        | `False`            | Enable debug mode.                                         |

### Parameter Tradeoffs

**SimHash distance threshold:**
- Lower (e.g., 5): Only catches nearly identical reposts.
- Higher (e.g., 20): Catches paraphrased content but may produce false positives.
- Recommendation: Start with 15, adjust if too many or too few duplicates.

**Cosine similarity threshold:**
- Lower (e.g., 0.6): Identifies loosely related posts. Useful for broad
  similarity mapping but noisy.
- Higher (e.g., 0.9): Only the most semantically identical pairs. Very precise
  but may miss paraphrases.
- Recommendation: 0.8 balances precision and recall well for LinkedIn posts.

**Number of clusters (k):**
- Too few (e.g., 2): Clusters are too broad -- each contains many unrelated
  subtopics. The bubble score will appear artificially diverse.
- Too many (e.g., 15): Clusters become noise. Single posts form their own
  "cluster." The bubble score becomes unreliable.
- Recommendation: Let the silhouette score choose k automatically (range 2-8),
  or use the default of 5 as a reasonable starting point.

**Embedding model:**
- `all-MiniLM-L6-v2` (384-dim, ~80 MB): Fast, good quality, the default.
- `all-mpnet-base-v2` (768-dim, ~420 MB): Better quality (higher scores on
  STS benchmarks) but 5x larger and slower. Recommended if accuracy is
  critical and resources are available.
- `all-MiniLM-L12-v2` (384-dim, ~120 MB): Same dimensionality as L6 but
  12 transformer layers instead of 6. Slight quality improvement.

---

## 12. Tradeoffs and Future Directions

### 12.1 Current Tradeoffs

1. **Entropy thresholds are heuristic.** The 0.30 and 0.60 cutoffs for "strong
   bubble" / "moderate" / "diverse" are somewhat arbitrary. They could be
   calibrated with empirical data from real LinkedIn feeds.

2. **K-Means assumes spherical clusters.** In 384-dimensional embedding space,
   semantic clusters may be non-spherical. DBSCAN or HDBSCAN could capture
   irregular cluster shapes, but K-Means with silhouette selection works well
   enough in practice.

3. **Pairwise comparison is O(N^2).** For both SimHash and cosine similarity,
   all pairs are compared. For large feeds (>10,000 posts), this may become
   slow. Approximate nearest neighbor (e.g., FAISS) could accelerate this.

4. **No temporal analysis.** The current pipeline treats all posts equally. A
   future version could weight recent posts more heavily or track how the
   bubble score changes over time.

5. **Single language.** The TF-IDF stop words list is English-only. The
   embedding model handles multilingual text to some degree, but cluster
   labeling would degrade for non-English feeds.

### 12.2 Potential Improvements

- **HDBSCAN** for automatic cluster count without the need for silhouette
  sweeps, plus built-in noise detection.
- **FAISS** for approximate nearest neighbor search to handle larger datasets.
- **Topic modeling** (BERTopic, LDA) as an alternative to K-Means + TF-IDF
  for richer topic descriptions.
- **Temporal scoring** to measure whether the bubble is growing or shrinking
  over time.
- **Interactive frontend** consuming the Plotly JSON to provide a full
  dashboard experience.

---

## Appendix: Key Source Files Reference

| File                                           | Purpose                                      |
|------------------------------------------------|----------------------------------------------|
| `backend/processing/text_cleaner.py`           | Text preprocessing (URL, HTML, whitespace)   |
| `backend/similarity/simhash_analyzer.py`       | SimHash fingerprinting and Hamming distance   |
| `backend/similarity/embedding_generator.py`    | Sentence embedding generation                |
| `backend/similarity/cosine_similarity.py`      | Cosine similarity matrix and pair detection  |
| `backend/clustering/topic_clusterer.py`        | K-Means clustering and silhouette selection  |
| `backend/clustering/cluster_labeler.py`        | TF-IDF cluster labeling                      |
| `backend/metrics/bubble_score.py`              | Normalized Shannon entropy bubble score      |
| `backend/visualization/umap_projector.py`      | UMAP 2D dimensionality reduction             |
| `backend/visualization/chart_builder.py`       | Plotly chart generation (scatter, pie, gauge)|
| `backend/core/config.py`                       | Tunable parameters and settings              |
| `backend/services/analysis_service.py`         | Pipeline orchestration                       |
| `backend/services/similarity_service.py`       | Lexical + semantic similarity service        |
| `backend/services/clustering_service.py`       | Clustering + labeling service                |
| `backend/services/bubble_score_service.py`     | Bubble score computation service             |
| `backend/services/visualization_service.py`    | Visualization generation service             |
