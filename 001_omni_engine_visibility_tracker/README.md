# ⬡ Omni-Engine Visibility & Attribution Intelligence

![Screenshot](asset/1.PNG)

**Omni-Engine Visibility Tracker** is an industrial-grade application designed to track brand visibility and attribution across major Generative AI search engines (Gemini, Perplexity, and SearchGPT). Developed by **HSINI MOHAMED**, this tool provides real-time insights into how LLMs source information and cite authorities.

---

## 🚀 Quick Start

### 1. Installation
Ensure you have Python 3.12+ installed. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Launch the Program
Run the main application:

```bash
python main.py
```

---

## 🛠️ Features

- **Multi-Provider Intelligence:** Simultaneously query Gemini, Perplexity, and SearchGPT.
- **Attribution Extraction:** Automatically identifies URLs, domains, author names, and document titles from AI responses.
- **Semantic Proximity Engine:** Computes the "Semantic Score" between your query and the AI's response using `sentence-transformers`.
- **Industrial GUI:** Sleek "Cyber-Pentagon" aesthetic with a high-performance multi-tab dashboard.
- **Interactive Visuals:** Dynamic **Sunburst Charts** to visualize attribution distribution across the web.
- **Executive Exports:** Generate professional **PDF Executive Summaries** and **JSON-LD Structured Data** for SEO and reporting.

---

## 📂 Project Structure

- `main.py`: The primary GUI entry point (CustomTkinter).
- `core/`: The logic engine.
    - `engine.py`: Attribution and Semantic processing.
    - `providers.py`: API integration with live and demo fallbacks.
    - `exports.py`: PDF and JSON-LD generation logic.
    - `models.py`: Data structures and design tokens.
- `requirements.txt`: List of Python dependencies.

---

## 📖 How to Use

1. **Query Input:** Enter a keyword or search phrase in the "QUERY ENGINE" box.
2. **Provider Selection:** Toggle which AI engines you want to analyze.
3. **API Setup:** Input your API keys in the sidebar. If left empty, the tool runs in **Demo Mode** with realistic pre-cached data.
4. **Execute Scan:** Click **[O] EXECUTE SCAN** to begin. The "System Log" will show real-time progress.
5. **Analyze Results:**
    - **Dashboard:** View high-level KPIs (Attributions, Domains, Semantic Scores).
    - **Sunburst:** Click to generate a browser-based interactive chart of mentions.
    - **Attribution Log:** Review every single source cited by the LLMs.
6. **Export:** Use the sidebar buttons to save a **PDF Summary** for stakeholders or **JSON-LD** for technical integration.

---

## ⚖️ License
Developed by **HSINI MOHAMED**. All rights reserved. Optimized for high-performance AI Search Orchestration.
