# Technical Documentation: Agentic GEO-Schema Architect

![Screenshot](asset/1.PNG)

![Agentic GEO-Schema Architect Mockup](assets/mockup.png)

## 1. Overview
The Agentic GEO-Schema Architect is a specialized "Search Intelligence" tool designed to automate the creation of high-fidelity JSON-LD. In the era of Generative Engine Optimization (GEO), structured data is the primary bridge between static websites and LLM knowledge graphs.

## 2. Technical Architecture

### 2.1 PySide6 GUI (Qt for Python)
The application uses a **Dark IDE** aesthetic:
- **Editor:** A custom `QTextEdit` subclass integrated with `QSyntaxHighlighter`.
- **Highlighter:** Uses `QRegularExpression` to identify JSON keys and values, providing a developer-friendly experience.
- **Bento Panel:** A grid-based layout using `QFrame` and `QGridLayout` to present high-level metadata (Model version, Compliance score).

### 2.2 Agentic Workflow
The system follows a 3-stage pipeline:
1. **Extraction (Spacy):** Uses the `en_core_web_sm` model to extract entities (Person, Org, GPE). This provides the "Context" for the schema.
2. **Generation (Gemini Pro):** The extracted entities and URL content are sent to Gemini with a specialized system prompt to generate compliant JSON-LD.
3. **Validation:** Pings a simulation of the Google Rich Results API to estimate a compliance score.

### 2.3 Async Execution
The entire workflow runs inside a `QThread` (ArchitectWorker). This ensures the UI remains responsive and the "Bento" status labels update in real-time while network-heavy crawling and LLM processing occur.

## 3. Compliance Standards
The architect is programmed to prioritize:
- **Nesting:** Proper parent-child relationships between entities (e.g., Organization as the author of a WebPage).
- **Mandatory Fields:** Ensures that all required properties for Google Search (e.g., `headline`, `image`, `author` for Articles) are present.
- **JSON-LD Syntax:** Strictly adheres to the RFC 7159 standard.

## 4. Troubleshooting
- **Missing Spacy Model:** The application automatically attempts to download `en_core_web_sm` on the first launch if it's missing.
- **API Key:** Ensure `GEMINI_API_KEY` is set as an environment variable or updated in `core/architect.py`.

---
**Developer:** HSINI MOHAMED
**Version:** 1.0.0
**Project ID:** 5
