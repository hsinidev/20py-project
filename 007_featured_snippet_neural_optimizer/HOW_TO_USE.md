# HOW TO USE: Featured-Snippet Neural Optimizer

![Screenshot](asset/1.PNG)


## 1. Setup
### Prerequisites
- Python 3.12+
- WxPython (Phoenix)

### Installation
```bash
pip install -r requirements.txt
```

## 2. Operation
1. **Launch the Optimizer**:
   ```bash
   python main.py
   ```
2. **Optimization Workflow**:
   - **Input Content**: Paste your draft article into the 'Before' window.
   - **Analyze**: Click the deconstruction button to see the sentence-level breakdown.
   - **Optimize**: Choose between 'Step-by-step' (Gemini) or 'Concise Fact' (Perplexity) rewriting modes.
3. **Review Scores**:
   - Monitor the **GEO Confidence Score** in the sidebar. Adjust content until the score reaches 85+.
4. **Export**:
   - Use the `EXPORT TO HTML` button to save your optimized snippet with semantic HTML5 markup.

## 3. Troubleshooting
- **Color Visibility**: The application uses an Agency-Modern theme (Deep Navy). If text is hard to read, ensure your display settings are set to high contrast.
- **NLTK Data**: The tool includes offline fallbacks, but for best results, ensure an active internet connection on first run to download NLTK resources.

---
**Developer:** HSINI MOHAMED
**Category:** GEO & AI-Search Orchestration
