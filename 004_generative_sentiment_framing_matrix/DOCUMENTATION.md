# Technical Documentation: Generative Sentiment & Framing Matrix

![Screenshot](asset/1.PNG)

## 1. Overview
The Generative Sentiment & Framing Matrix is a specialized NLP tool for measuring "Brand Framing" in AI environments. While sentiment measures *positivity*, framing measures *positioning*. This tool maps brands into a multi-dimensional matrix to show how they are perceived by generative engines.

## 2. Technical Architecture

### 2.1 Neumorphic Design (KivyMD)
The application uses a **Neumorphic (soft-UI)** approach:
- **Design:** Created using Kivy's `canvas` instructions for subtle shadows and light-source simulation.
- **Colors:** Charcoal (`#1a1a1a`) with Lavender (`#b39ddb`) accents.

### 2.2 NLP Logic (`core/classifier.py`)
- **Model:** `distilbert-base-uncased-finetuned-sst-2-english`.
- **Logic:** The classifier analyzes sentiment first, then applies a heuristic keyword-frequency mapping to identify "Framing Bias."
    - **Premium Leader:** High frequency of authority/quality keywords + positive sentiment.
    - **Budget Alternative:** High frequency of cost/alternative keywords + neutral/positive sentiment.
    - **Technical Authority:** High frequency of complexity/specialization keywords.

### 2.3 3D Matrix Visualization (`core/matrix.py`)
Uses **Plotly Express** to render an interactive 3D scatter plot.
- **X-Axis:** Sentiment (-1 to 1).
- **Y-Axis:** Authority (0 to 1, derived from confidence scores).
- **Z-Axis/Color:** Framing Category.
- **Output:** Generates a standalone HTML file and opens it via the system's default browser.

### 2.4 Tone-Shift Simulator
Provides a theoretical model for how API temperature settings (0.0 to 2.0) influence the "Framing Flux." This is critical for understanding if an LLM's bias is stable or volatile.

## 3. SEO Metadata
The application includes a logic layer for generating **JSON-LD Review Snippets**. This allows brands to showcase "AI-Analyzed" sentiment data in search engine rich results, proving their status as a "Leader" or "Trusted Authority" within AI contexts.

## 4. Dependencies & Hardware
- **PyTorch:** Required for the transformer model.
- **GPU:** While optional, a CUDA-capable GPU will significantly speed up DistilBERT inference.
- **KivyMD:** The framework for the neumorphic interface.

---
**Developer:** HSINI MOHAMED
**Version:** 1.0.0
**Project ID:** 4
