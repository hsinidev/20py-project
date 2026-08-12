# Technical Documentation: LLM Citation Integrity Auditor

![Screenshot](asset/1.PNG)

## 1. Overview
The LLM Citation Integrity Auditor is a verification framework for evaluating the "Grounding" of Large Language Models. It solves the problem of "Hallucination via Citation," where an LLM provides a link that does not actually contain the information it claims.

## 2. Technical Architecture

### 2.1 The "Medical-Laboratory" Design System
The UI is built using **PyQt6** and stylized via **QSS (Qt Style Sheets)** to mimic a clinical laboratory environment:
- **Base Color:** `#f8fafc` (Slate-White)
- **Primary Accent:** `#10b981` (Emerald Green)
- **Alert Color:** `#ef4444` (Clinical Red)
- **Typography:** Segoe UI / Consolas (for logs)

### 2.2 Async Scraper (`core/scraper.py`)
Uses `httpx` and `BeautifulSoup4` to perform non-blocking web requests. 
- **HTML Sanitization:** Automatically strips `<script>`, `<style>`, and `<nav>` tags to prevent noise in the similarity analysis.
- **Concurrency:** Uses `asyncio.gather` to fetch all cited sources in parallel, significantly reducing audit time.

### 2.3 Similarity Engine (`core/similarity.py`)
- **Primary Engine:** `sentence-transformers/all-MiniLM-L6-v2`. This model transforms claims and source paragraphs into 384-dimensional vectors.
- **Verification:** Cosine similarity is calculated. 
    - **Score > 0.7:** High confidence grounding.
    - **Score < 0.4:** Potential hallucination or citation mismatch.

### 2.4 Audit Orchestrator (`core/auditor.py`)
- **Extraction:** Uses complex regex to identify inline citations and bottom-of-page reference blocks.
- **Scoring Logic:** Claims are segments of the response text associated with specific URLs. Each claim is verified individually to provide a granular "Grounding Map."

## 3. SEO & Schema Integration
The application is pre-configured to export results with **'Verified By' Schema markup** (JSON-LD), allowing audited content to display "Fact Checked" snippets in search engine results.

## 4. Performance Tuning
- **SQLite-WAL:** The app is designed to support a SQLite Write-Ahead Logging backend for persistent audit histories (to be enabled in v1.1).
- **Multi-Threading:** The GUI remains responsive during heavy similarity computations by offloading logic to a `QThread`.

---
**Developer:** HSINI MOHAMED
**Version:** 1.0.0
**Project ID:** 2
