# HOW TO USE: Omni-Engine Visibility Tracker

![Screenshot](asset/1.PNG)

## 1. Setup
### Prerequisites
- Python 3.12+
- Playwright

### Installation
```bash
pip install -r requirements.txt
playwright install chromium
```

## 2. Operation
1. **Launch the Application**:
   ```bash
   python main.py
   ```
2. **Dashboard Navigation**:
   - **Query Input**: Enter the search term you wish to track across LLMs.
   - **Provider Toggles**: Select which engines to query (Gemini, Perplexity, SearchGPT).
   - **Execute**: Click the primary dispatch button to start the multi-threaded crawl.
3. **Analyze Results**:
   - **Sunburst Chart**: View semantic visibility distribution.
   - **Attribution Log**: Review extracted URLs and author metadata.

## 3. Customization
Modify the `config` module in the `core/` directory to update proxy settings or user-agent strings.

---
**Developer:** HSINI MOHAMED
**Category:** GEO & AI-Search Orchestration
