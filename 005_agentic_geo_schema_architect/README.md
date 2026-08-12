# 🏗️ Agentic GEO-Schema Architect

![Screenshot](asset/1.PNG)

![Agentic GEO-Schema Architect Mockup](assets/mockup.png)

**Agentic GEO-Schema Architect** is an autonomous industrial-grade tool for generating deeply nested, 100% compliant JSON-LD schema for search engines. Developed by **HSINI MOHAMED**, it leverages advanced NLP and Generative AI to architect schema that maximizes visibility in AI search environments (GEO).

---

## 🚀 Quick Start

### 1. Installation
Requires Python 3.12+. Install the PySide6 and NLP stack:

```bash
pip install -r requirements.txt
```

### 2. Launch the Architect
Run the PySide6 application:

```bash
python main.py
```

---

## 🛠️ Features

- **IDE-Grade GUI:** A professional interface featuring a monospaced code editor with real-time JSON syntax highlighting.
- **Bento-Grid Dashboard:** A modern, high-density settings panel for monitoring model status and compliance scores.
- **Autonomous Crawler:** Built-in engine to fetch and parse URL content for entity discovery.
- **Spacy NER Integration:** Uses Named Entity Recognition to identify relationships, organizations, and key personas on the page.
- **Gemini Pro Architect:** Leverages Google's Gemini Pro to generate complex, nested schema types (WebPage, FAQ, Organization, Speakable).
- **Google Compliance Ready:** Designed to meet 100% rich results validation standards for maximum indexing potential.

---

## 📂 Project Structure

- `main.py`: The primary PySide6 application entry point.
- `core/`:
    - `nlp.py`: Spacy entity extraction and NLP logic.
    - `architect.py`: Gemini Pro integration for JSON-LD generation.
- `ui/`:
    - `editor.py`: Monospaced editor with custom Pygments highlighting.
- `requirements.txt`: Project dependencies.

---

## 📖 How to Use

1. **Target Input:** Paste the target URL into the input field at the top.
2. **Execute:** Click **EXECUTE ARCHITECT**. The agent will crawl the page and extract entities.
3. **Review:** The generated JSON-LD will appear in the central code editor with syntax highlighting.
4. **Deploy:** Copy the code directly into your website's `<head>` or Google Tag Manager.

---

## ⚖️ License
Developed by **HSINI MOHAMED**. Part of the 1,000 Python Scripts Enterprise Collection. Engineered for AI-Search Dominance.
