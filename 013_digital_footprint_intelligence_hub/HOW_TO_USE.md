# Digital Footprint Intelligence Hub (Scalable Edition) v2.0

## Overview
The **Digital Footprint Intelligence Hub** is a professional-grade OSINT (Open Source Intelligence) platform designed for cybersecurity researchers, private investigators, and digital forensics experts. It automates the discovery of a target's online presence across 400+ platforms and performs advanced Google Dorking to extract sensitive metadata and directory exposures.

## How to Use
1. **Prerequisites**:
   - Python 3.8+
   - Install dependencies: `pip install -r requirements.txt`
2. **Launch**:
   - Run `python main.py` from the project root.
3. **Execution**:
   - Enter a target username or full name in the "Global Search" bar.
   - Click **INITIATE SCAN**.
   - Watch the live **Entity Relation Mapping** canvas as nodes are discovered and linked in real-time.
4. **Export**:
   - Click the export icon in the sidebar to generate a comprehensive intelligence dossier in JSON, CSV, and Text formats.

## Features
- **Asynchronous Scanner**: High-concurrency engine (limit 50) for rapid platform checking.
- **Interactive Graph Canvas**: Real-time node physics using NetworkX for relationship visualization.
- **Advanced Dorking**: Automated Google Dorks targeting filetypes (PDF, XLSX) and sensitive paths.
- **Local Persistence**: Full investigation history saved in SQLite3.
- **Glassmorphism UI**: High-fidelity dark mode with CRT-scanline overlays for a professional "War Room" aesthetic.

---
**CREDIT**: Developed by HSINI MOHAMED.
