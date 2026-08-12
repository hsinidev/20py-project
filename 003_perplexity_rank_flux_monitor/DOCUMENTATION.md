# Technical Documentation: Perplexity Rank Flux Monitor

![Screenshot](asset/1.PNG)


## 1. Overview
The Perplexity Rank Flux Monitor is a high-frequency tracking tool for measuring the "Source Position" of domains within the Perplexity.ai search carousel. Unlike traditional Google SEO, GEO (Generative Engine Optimization) requires tracking specific source attribution blocks that update dynamically.

## 2. Technical Architecture

### 2.1 Dear PyGui (GPU Accelerated)
The application utilizes **Dear PyGui (DPG)**, a wrapper around Dear ImGui. 
- **Performance:** UI rendering is offloaded to the GPU (DirectX11/Metal), ensuring that complex charts and live tables do not lag even with high-frequency updates.
- **Styling:** Controlled via a custom `global_theme` which implements the "Trading-Floor" aesthetic using high-contrast neon colors.

### 2.2 Selenium Stealth & Automation (`core/monitor.py`)
- **Detection Evasion:** Utilizes `selenium-stealth` to mask automated browser fingerprints. It spoofs WebGL vendors, renderers, and window properties.
- **Scraping Strategy:** The monitor identifies the `Sources` carousel elements on Perplexity.ai and maps the ordered list of domains to their rank positions (1-10).

### 2.3 SQLModel & SQLite-WAL (`core/db.py`)
- **Concurrency:** The database is initialized with `PRAGMA journal_mode=WAL;`. This allows multiple threads (UI and Scraper) to read and write simultaneously without lock contention.
- **Persistence:** All rank shifts are logged with microsecond precision, enabling long-term volatility analysis.

### 2.4 Probability Forecasting (`core/forecast.py`)
- **Algorithm:** Uses a momentum-based probability model. If a domain's average position is moving toward 1 with high velocity, the "BULL" probability increases.
- **Volatility Metric:** Calculated as the standard deviation of rank positions over the last 10 ticks.

## 3. UI Layout
- **Rank Ladder (Left):** Real-time table showing current top-10 domains for the selected keyword.
- **Sparkline (Top Right):** Visual representation of the average rank drift across the entire keyword pool.
- **Telemetry (Bottom Right):** Console for low-level logging of proxy status, request times, and automation errors.

## 4. Key UX Workflows
- **Panic Alerts:** Triggered if a monitored "Top Tier" domain drops more than 5 positions in a single tick.
- **Monitoring Loop:** Runs in a separate daemon thread to ensure the DPG rendering loop remains at a constant high frame rate.

---
**Developer:** HSINI MOHAMED
**Version:** 1.0.0
**Project ID:** 3
