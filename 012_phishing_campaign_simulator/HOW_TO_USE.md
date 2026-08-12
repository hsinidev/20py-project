# How to Use: Phishing Campaign Simulator

## Setup
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Launch Application**:
   ```bash
   python main.py
   ```

## Creating a Campaign
1. Acknowledge the **Legal Splash Screen**.
2. Navigate to **Campaign Builder**.
3. Enter a descriptive **Campaign Name**.
4. Configure your **Email Subject** and **HTML Template**.
   - *Important*: Ensure your template includes the `{{LINK}}` placeholder for tracking.
5. Add target emails in the **Target List** field (one per line).
6. Click **Launch Simulation Campaign**.

## Analyzing Results
1. Return to the **Dashboard** to view real-time metrics.
2. The bar chart will update as the background Flask server receives clicks.
3. Once the campaign is complete, go to **Audit Reports** and click **Generate Latest Report** to export a professional PDF.

## Note on SMTP
For real email delivery, configure your SMTP settings in `core/mailer.py`. By default, the tool runs in **Simulation Mode** (Logging only).
