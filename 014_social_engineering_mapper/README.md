# Social Engineering Vulnerability Mapper (Enterprise Edition)

![Cover](asset/cover.png)

## 🛡️ Overview
The **Social Engineering Vulnerability Mapper** is a strategic intelligence tool designed to audit an organization's digital exposure. Developed by **HSINI MOHAMED**, it maps organizational hierarchies and identifies PII (Personally Identifiable Information) leaks that could be exploited in social engineering campaigns.

## 🚀 Key Features
- **ATQA Architecture**: Asynchronous Task-Queue Architecture for parallel data extraction.
- **Cognitive NLP**: Spacy-driven analysis to detect "Social Vulnerabilities" in public bios and repositories.
- **Live Risk Matrix**: Interactive Plotly heatmaps embedded via `QtWebEngine`.
- **Headless Scraping**: Playwright cluster for stealthy, multi-instance data gathering.
- **Executive Reporting**: Automated Jinja2 templates for professional HTML vulnerability audits.
- **Corporate-Tactical UI**: Strategic Minimalist design with Burnt Orange accents.

## 🛠️ Tech Stack
- **UI**: PySide6 (Qt), QtWebEngine
- **Analysis**: Spacy (NLP), Pandas, Plotly
- **Scraping**: Playwright (Headless)
- **Reporting**: Jinja2

## 📥 Installation
```bash
pip install -r requirements.txt
playwright install chromium
python -m spacy download en_core_web_sm
```

## 📜 License
Developed for authorized enterprise security auditing.
**Credit**: Developed by HSINI MOHAMED.
