# Project Prompt --- "What Is Your Bubble?"

## Overview

**What Is Your Bubble?** is a data analysis and visualization tool that
helps users understand the information bubble in their LinkedIn feed.\
The project collects a sample of posts from a user's feed, analyzes
their lexical and semantic similarity, and groups them into topic
clusters.\
The final output reveals what themes dominate the user's feed and how
concentrated their information bubble is.

The goal is to provide users with a clear, data‑driven view of the kinds
of content shaping their professional information environment.

------------------------------------------------------------------------

# Core Idea

1.  Collect posts from the user's LinkedIn feed
2.  Measure similarity between posts
3.  Detect clusters of topics
4.  Quantify how concentrated the feed is
5.  Visualize the user's "bubble"

Example output:

    Your LinkedIn Bubble

    AI / Automation        41%
    Startup Motivation     27%
    Productivity           16%
    Career Advice          11%
    Other                   5%

    Bubble Diversity Score: 0.32

------------------------------------------------------------------------

# Key Features

## 1. Feed Scraping via Chrome Extension

A Chrome extension collects posts from the user's LinkedIn feed while
the user scrolls.

Collected fields:

-   post_id
-   author
-   text
-   timestamp
-   engagement metrics (optional)

The extension exports the dataset as JSON and sends it to the analysis
backend.

------------------------------------------------------------------------

## 2. Lexical Similarity Detection

The project uses **SimHash** to detect posts that are structurally
similar or near‑duplicates.

This identifies repetitive content patterns like:

• "10 lessons from building a startup"\
• "10 things startups taught me"

Similarity is measured using **Hamming Distance**.

Purpose:

Detect repetitive phrasing and content templates in the feed.

------------------------------------------------------------------------

## 3. Semantic Similarity Analysis

Each post is converted into a vector embedding representing its meaning.

Similarity between posts is calculated using **cosine similarity**.

This allows the system to group posts discussing similar ideas even if
the wording differs.

Example:

"AI will replace repetitive jobs"\
"Automation will eliminate routine work"

These posts would be clustered together semantically.

------------------------------------------------------------------------

## 4. Topic Clustering

Posts are grouped using **K‑Means clustering**.

Typical clusters may include:

-   AI / automation
-   startup advice
-   productivity hacks
-   corporate career growth
-   technology trends

Cluster proportions define the user's bubble.

------------------------------------------------------------------------

## 5. Bubble Diversity Score

The project calculates a **Bubble Diversity Score** based on how evenly
posts are distributed across clusters.

Example interpretation:

    Score < 0.30 → Strong information bubble
    Score 0.30–0.60 → Moderate diversity
    Score > 0.60 → Diverse feed

This metric quantifies how concentrated the user's feed is.

------------------------------------------------------------------------

## 6. Visualization

Embeddings are projected into 2D space using **UMAP** to generate a
visual map of the feed.

Each dot represents a post.

Clusters reveal the dominant topics shaping the user's information
environment.

Visualization options:

-   Topic map
-   Cluster distribution chart
-   Bubble concentration indicator

------------------------------------------------------------------------

# System Architecture

    Chrome Extension
            ↓
    LinkedIn Feed Scraper
            ↓
    Dataset (JSON / CSV)
            ↓
    Python Backend Analysis
            ↓
    Similarity Computation
            ↓
    Clustering + Bubble Score
            ↓
    Visualization Dashboard

------------------------------------------------------------------------

# Tech Stack

## Frontend

Chrome Extension

Technologies:

-   JavaScript
-   Chrome Extension API
-   DOM scraping
-   JSON export

Responsibilities:

-   Collect posts from the LinkedIn feed
-   Export dataset for analysis

------------------------------------------------------------------------

## Backend

Python

Framework:

-   FastAPI

Responsibilities:

-   Receive dataset
-   Process posts
-   Run similarity algorithms
-   Generate clusters
-   Compute bubble metrics

------------------------------------------------------------------------

## Data Processing Libraries

Python libraries:

-   pandas --- dataset manipulation
-   numpy --- numerical operations

------------------------------------------------------------------------

## Similarity Algorithms

-   simhash --- lexical similarity detection
-   sentence-transformers --- semantic embeddings
-   scikit-learn --- clustering and similarity computation

------------------------------------------------------------------------

## Dimensionality Reduction

-   umap-learn

Used to create the topic map visualization.

------------------------------------------------------------------------

## Visualization

Possible tools:

-   plotly
-   streamlit
-   matplotlib

Purpose:

Provide an intuitive visual representation of the user's information
bubble.

------------------------------------------------------------------------

# Example Project Structure

    bubble-project/

    scraper/
        chrome_extension/

    data/

    backend/
        api.py

    processing/
        clean_posts.py

    similarity/
        simhash_analysis.py
        embedding_generation.py

    clustering/
        topic_clustering.py

    metrics/
        bubble_score.py

    visualization/
        topic_map.py

------------------------------------------------------------------------

# Project Goal

The ultimate goal of **What Is Your Bubble?** is to make information
bubbles visible and measurable.

By combining scraping, NLP similarity analysis, clustering, and
visualization, the project reveals how algorithmic feeds shape the
information users consume.
