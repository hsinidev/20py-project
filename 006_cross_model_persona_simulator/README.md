# 🎭 Cross-Model Persona Bias Simulator

![Screenshot](asset/1.PNG)


![Cross-Model Persona Bias Simulator Mockup](assets/mockup.png)

**Cross-Model Persona Bias Simulator** is a research-grade tool for detecting and analyzing behavioral biases across different Large Language Models. Developed by **HSINI MOHAMED**, the application allows researchers to simulate how various "Personas" influence the empathy, caution, and directness of AI responses in a side-by-side A/B testing environment.

---

## 🚀 Quick Start

### 1. Installation
Requires Python 3.12+. Install the Flet and LLM orchestration stack:

```bash
pip install -r requirements.txt
```

### 2. Launch the Simulator
Run the Flet application:

```bash
python main.py
```

---

## 🛠️ Features

- **A/B Testing UI:** A sophisticated split-pane layout using Burgundy and Warm Grey accents for high-clarity comparisons.
- **Multi-Model Dispatch:** Simultaneously query GPT-4, Claude 3.5, and Gemini 1.5 with a single click.
- **Persona Simulation:** Test biases across predefined personas (e.g., High-Net-Worth Investor, Single Mother, Software Engineer).
- **Behavioral Scoring:** Dynamic analysis of "Empathy", "Caution", and "Directness" for every response.
- **Radar Telemetry:** Visual indicators for comparing model performance and behavioral alignment.
- **Research Export:** Standardized CSV export for further statistical analysis in academic or commercial research.

---

## 📂 Project Structure

- `main.py`: The primary Flet (Flutter-based) application entry point.
- `core/`:
    - `engine.py`: Multi-LLM dispatch and API orchestration.
    - `models.py`: Data schemas and A/B testing theme tokens.
- `assets/`: Project visual assets and mockups.
- `requirements.txt`: Project dependencies.

---

## 📖 How to Use

1. **Persona Selection:** Choose a target persona from the dropdown menu to set the context.
2. **Input Prompt:** Enter the query or scenario you wish to test for bias.
3. **Analyze:** Click **DISPATCH CROSS-MODEL ANALYSIS**. The engine will query the active models in parallel.
4. **Compare:** Review the side-by-side results in the split-pane view, paying close attention to the percentage scores for empathy and directness.
5. **Evaluate:** Use the visual progress bars to identify which model aligns most closely with your target communication style.

---

## ⚖️ License
Developed by **HSINI MOHAMED**. Part of the 1,000 Python Scripts Enterprise Collection. Engineered for AI Behavioral Research.
