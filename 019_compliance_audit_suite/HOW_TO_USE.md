# How to Use: Automated Compliance Audit Suite

## 1. Prerequisites
- Python 3.10+
- Administrator privileges (required for some technical control checks like Registry and Service status).
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## 2. Starting an Audit
1. Run the application: `python main.py`.
2. Select your framework (e.g., ISO 27001).
3. Follow the **10-Step Progress Stepper** at the top of the dashboard.

## 3. Control Validation
- **Automatic Controls**: The system will scan your configuration and report a PASS/FAIL status immediately.
- **Manual Controls**: For policies and operational procedures, click **Details** to upload evidence or manually attest to the control's implementation.

## 4. Evidence Management
- Associate policy documents (PDF/DOCX) with specific controls in the Evidence step.
- The system will calculate a weighted score based on the criticality of the validated controls.

## 5. Generating Reports
1. Complete all required steps in the stepper.
2. Click **GENERATE EXECUTIVE REPORT**.
3. Choose your format (PDF or DOCX).
4. The report will be saved in the `reports/` directory, ready for management review.

---
**Developed by HSINI MOHAMED.**
