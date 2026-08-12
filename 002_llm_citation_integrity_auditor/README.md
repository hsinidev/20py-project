# 🔬 LLM Citation Integrity & Truth-Grounding Auditor

![Screenshot](asset/1.PNG)

**LLM Citation Integrity Auditor** is a professional-grade clinical verification tool designed to audit AI-generated content for grounding accuracy. Developed by **HSINI MOHAMED**, this application cross-references LLM claims against live web sources using semantic vector analysis and automated self-correction loops.

---

## 🚀 Quick Start

### 1. Installation
Requires Python 3.12+. Install the clinical tech stack:

```bash
pip install -r requirements.txt
```

### 2. Launch the Auditor
Run the PyQt6 application:

```bash
python main.py
```

---

## 🛠️ Features

- **Medical-Laboratory UI:** High-density, clinical-white interface optimized for data precision and readability.
- **Asynchronous Fact-Checking:** Concurrently fetches source HTML from multiple citations without blocking the UI.
- **Semantic Truth-Grounding:** Uses `Sentence-Transformers` to compute cosine similarity between the LLM's claim and the actual source text.
- **Grounding Scorecard:** Instant visual KPIs for Overall Grounding, Claim Count, and System Status.
- **Hallucination Detection:** Color-coded grid identifying "Verified" vs. "Hallucination" segments.
- **Self-Correction Logic:** Capable of identifying which specific citation in a multi-source claim supports or contradicts the text.

---

## 📂 Project Structure

- `main.py`: The primary PyQt6 application entry point.
- `core/`:
    - `auditor.py`: LangChain-ready audit orchestration.
    - `scraper.py`: Async HTTP fetching and HTML sanitization.
    - `similarity.py`: Semantic vector computation engine.
    - `models.py`: Data schemas and "Medical-Laboratory" theme tokens.
- `ui/`:
    - `styles.py`: QSS implementation of the Fluent Design theme.
- `requirements.txt`: Project dependencies.

---

## 📖 How to Use

1. **Input Claim:** Paste an LLM response containing citations (e.g., `[1]` or `https://...`) into the "LLM Response" box.
2. **Execute Audit:** Click **EXECUTE AUDIT**.
3. **Analyze Score:** 
    - **Healthy (80%+):** Claims are well-supported by sources.
    - **Unstable (40-80%):** Partial support or cherry-picked citations.
    - **Critical (<40%):** High likelihood of hallucinations or broken links.
4. **Review Grid:** Examine the "Detailed Findings" tab to see exactly which claims failed the semantic check.

---

## ⚖️ License
Developed by **HSINI MOHAMED**. Part of the 1,000 Python Scripts Enterprise Collection. Optimized for LLM Accuracy and Content Safety.
