from flask import Flask, render_template, request, redirect
import jwt
import datetime
import threading

app = Flask(__name__)
SECRET_KEY = "AUDIT_SECRET_2026"

# This list would ideally be stored in a shared state or DB
campaign_observer = None

@app.route('/track/<token>')
def track_click(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        campaign_id = data.get("cid")
        if campaign_observer:
            campaign_observer.log_click(campaign_id)
        return render_template('portal.html', cid=campaign_id, token=token)
    except:
        return "Invalid Audit Link", 403

@app.route('/submit', methods=['POST'])
def handle_submit():
    token = request.form.get("token")
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        campaign_id = data.get("cid")
        if campaign_observer:
            campaign_observer.log_compromised(campaign_id)
        return render_template('safety_training.html')
    except:
        return "Submission Failed", 403

def run_server(port=5000, observer=None):
    global campaign_observer
    campaign_observer = observer
    app.run(port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    run_server()
