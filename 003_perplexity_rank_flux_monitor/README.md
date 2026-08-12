# ⚡ Perplexity Rank Flux & Volatility Monitor

![Screenshot](asset/1.PNG)


**Perplexity Rank Flux Monitor** is a high-speed, GPU-accelerated tracking engine designed to monitor search result positions on Perplexity.ai. Developed by **HSINI MOHAMED**, this tool provides real-time "Trading-Floor" telemetry for digital marketers and SEO specialists focused on Generative Engine Optimization (GEO).

---

## 🚀 Quick Start

### 1. Installation
Requires Python 3.12+. Install the automation and monitoring stack:

```bash
pip install -r requirements.txt
```

### 2. Launch the Monitor
Run the Dear PyGui application:

```bash
python main.py
```

---

## 🛠️ Features

- **Trading-Floor GUI:** High-performance, GPU-accelerated interface with Neon Green/Red indicators on a deep black background.
- **Selenium Stealth Automation:** Bypasses bot detection on Perplexity.ai using specialized stealth drivers and randomized behavior patterns.
- **Live Rank Ladder:** A real-time split-view dashboard showing top-tier domain positions and their relative flux.
- **Volatility Sparklines:** Interactive DPG plots visualizing rank drift over time.
- **Panic Alert System:** Automated system notifications triggered when high-authority domains experience significant ranking drops.
- **Probability Forecasting:** Advanced predictive logic that estimates next-day rank shifts based on historical volatility patterns.
- **SQLite-WAL Persistence:** High-speed data logging using Write-Ahead Logging (WAL) for zero-latency concurrent writes.

---

## 📂 Project Structure

- `main.py`: The primary Dear PyGui application entry point.
- `core/`:
    - `monitor.py`: Selenium Stealth automation and scraping engine.
    - `forecast.py`: Rank shift probability and prediction logic.
    - `db.py`: SQLModel & SQLite-WAL database orchestration.
    - `models.py`: Data schemas and Trading-Floor color tokens.
- `ui/`:
    - `theme.py`: Dear PyGui global styling and theme configuration.
- `requirements.txt`: Project dependencies.

---

## 📖 How to Use

1. **Initialize:** Launch the program. The "System Telemetry" log will indicate the database status.
2. **Start Monitoring:** Click the **START MONITORING** button. The system will begin cycling through your keyword list.
3. **Analyze Flux:** 
    - **Green (+):** The domain is gaining authority/position.
    - **Red (-):** The domain is losing authority/position.
4. **Predictive Insights:** Check the **LIVE FLUX** indicator in the header to see the probability of the current trend continuing.
5. **Panic Reset:** If you encounter widespread ranking shifts, use the **PANIC RESET** button to clear temporary flux logs and recalibrate the baseline.

---

## ⚖️ License
Developed by **HSINI MOHAMED**. Part of the 1,000 Python Scripts Enterprise Collection. Engineered for High-Frequency SEO Monitoring.
