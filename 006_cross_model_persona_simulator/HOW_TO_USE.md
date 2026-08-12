# HOW TO USE: Cross-Model Persona Bias Simulator

![Screenshot](asset/1.PNG)


## 1. Setup
### Install Dependencies
Ensure you have Python 3.10+ and Ollama (for local testing) installed.
```bash
pip install -r requirements.txt
```

### Local Models (Ollama)
Ensure Ollama is running and you have at least one model pulled (e.g., `llama3`):
```bash
ollama run llama3
```

### API Keys (Cloud)
To use Cloud models (OpenAI or Gemini), you must enter your API keys directly in the application's configuration panel or set them as environment variables.

## 2. Running the Simulator
Launch the application:
```bash
python main.py
```

## 3. Analysis Workflow
1. **Configure Models**: Use the toggles to enable/disable Local or Cloud components. Select your desired models from the dropdowns.
2. **Define Personas**: Enter distinct personas (e.g., "Skeptical Auditor" vs "Visionary Investor").
3. **Input Prompt**: Enter a universal prompt to be sent to both models.
4. **Execute**: Click `EXECUTE A/B BIAS ANALYSIS`.
5. **Review Results**:
   - **Split-Pane View**: Compare responses side-by-side.
   - **Citation Divergence**: See the percentage of semantic difference calculated via SBERT.
   - **Semantic Heatmap**: View "Trigger Keywords" that highlight high-salience terms in the responses.

## 4. Troubleshooting
- **Ollama Error**: Ensure the Ollama service is running in your system tray.
- **Model Loading**: Use the `REFRESH` button if your local models don't appear in the dropdown.
- **Divergence at 50%**: This is the fallback value if SBERT (Sentence-Transformers) fails to load or process the text.

---
**Developer:** HSINI MOHAMED
**Category:** Generative Engine Optimization (GEO)
