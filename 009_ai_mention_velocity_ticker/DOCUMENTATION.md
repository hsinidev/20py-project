# DOCUMENTATION: AI Mention Velocity Ticker

![Screenshot](asset/1.PNG)

Version: 1.0.0
Author: HSINI MOHAMED

## Architectural Overview
The AI Mention Velocity Ticker is a high-performance monitoring tool designed to track the "velocity" of brand mentions across the neural search ecosystem. It is specifically built for Generative Engine Optimization (GEO) specialists who need to monitor real-time data influx that might influence RAG (Retrieval-Augmented Generation) systems.

## Technical Components
1. **Tkinter High-Speed Canvas**: The GUI utilizes a custom Canvas-based rendering engine for the scrolling marquee and histogram to ensure low CPU overhead even with frequent updates.
2. **Asynchronous Feed Processor**: A dedicated background thread handles the polling of RSS feeds (Google News, social signals) via `feedparser` to prevent GUI freezing.
3. **Intent-Filtering Heuristic**: The engine scans headlines for "High-Intent" keywords (benchmarks, launches, SOTA claims) that indicate high semantic value for LLM training and retrieval.
4. **Velocity Algorithm**: Mentions are tracked in a rolling 60-second window to calculate `MPM` (Mentions Per Minute).

## Key Metrics
- **Velocity (MPM)**: The speed at which the brand is being mentioned globally.
- **High-Intent Signals**: A count of mentions that are statistically likely to trigger an update in an LLM's internal knowledge base or RAG index.
- **Sentiment Flux**: Monitored via keyword clustering (simulated in v1.0).

## G-Tag Integration
The system includes a simulation of Google Tag tracking for outbound clicks on mentions, allowing for performance attribution within the GEO dashboard.
