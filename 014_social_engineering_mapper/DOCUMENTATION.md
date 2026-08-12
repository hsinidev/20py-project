# Technical Documentation: Social Engineering Vulnerability Mapper

## 1. Intelligence Gathering Layer
The system utilizes **Playwright** to orchestrate a cluster of headless browsers. This layer focuses on extracting raw text from professional networks, company directories, and public code repositories.

## 2. Cognitive Analysis Layer
- **NLP Engine**: Uses `Spacy` (en_core_web_sm) to perform Named Entity Recognition (NER). It specifically looks for `PERSON`, `ORG`, and `LOC` entities to map organizational footprints.
- **Vulnerability Detection**: Custom regex patterns analyze the extracted text for "vulnerability indicators" like tech stack mentions, internal project names, or specific deadlines.
- **Risk Scoring**: A vectorized scoring algorithm (Risk Index 0.0-1.0) weights PII exposure and technical leakage to rank department-level risk.

## 3. UI/GUI Architecture
- **PySide6**: The main framework for the tactical dashboard.
- **QtWebEngine**: A bridge used to render dynamic Plotly heatmaps. This allows the user to interactively explore high-exposure departments.
- **QSS Styling**: A global stylesheet enforces the "Corporate-Tactical" theme (Charcoal & Burnt Orange).

## 4. Scalability Logic
The application bypasses the Python GIL by utilizing `multiprocessing` for scraping clusters. Each scraping task runs in an isolated process, feeding results back to the UI thread via a task queue.

## 5. File Structure
- `app.py`: System bootstrapper.
- `scrapers/manager.py`: Playwright instance management.
- `analysis/nlp_engine.py`: Spacy entity and vulnerability logic.
- `analysis/risk_matrix.py`: Pandas correlation and matrix math.
- `ui/main_window.py`: PySide6 dashboard logic.
- `ui/web_view.py`: Plotly/WebEngine bridge.
- `exports/html_generator.py`: Jinja2 executive report builder.

---
**Developer**: HSINI MOHAMED
**Version**: 2.1.0
