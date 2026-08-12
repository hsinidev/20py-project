# How to Use: Social Engineering Vulnerability Mapper

## 1. Prerequisites
Ensure you have the following installed:
- Python 3.9+
- Pip dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Tooling setup:
  ```bash
  playwright install chromium
  python -m spacy download en_core_web_sm
  ```

## 2. Launching the Audit
1. Run the system: `python app.py`.
2. Enter target URLs (e.g., company LinkedIn profiles, About Us pages, or repository URLs) into the **STRATEGIC TARGETING** field.
3. Click **ADD TARGET** to build your audit queue.

## 3. Running the Analysis
1. Click **INITIATE GLOBAL AUDIT**.
2. Monitor the **Tactical Intelligence Feed** for real-time NLP results.
3. Observe the **Live Risk Matrix**; the heatmap will update as data for each department is synthesized.

## 4. Reporting
1. Once the audit is complete, the **GENERATE EXECUTIVE REPORT** button will activate.
2. Click it to produce a high-fidelity HTML report in the `exports/` folder.
3. Review the **Security Recommendations** to mitigate identified organizational exposures.

---
**Developed by HSINI MOHAMED.**
