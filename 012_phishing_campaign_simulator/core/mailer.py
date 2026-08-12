import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import jwt

class MailEngine:
    def __init__(self, smtp_server, port, user, password, secret_key="AUDIT_SECRET_2026"):
        self.smtp_server = smtp_server
        self.port = port
        self.user = user
        self.password = password
        self.secret_key = secret_key

    def send_campaign(self, campaign_id, targets, subject, body_template, callback=None):
        def worker():
            for target in targets:
                try:
                    # Create tracking token
                    token = jwt.encode({"cid": campaign_id, "email": target}, self.secret_key, algorithm="HS256")
                    tracking_link = f"http://localhost:5000/track/{token}"
                    
                    msg = MIMEMultipart()
                    msg['From'] = self.user
                    msg['To'] = target
                    msg['Subject'] = subject
                    
                    body = body_template.replace("{{LINK}}", tracking_link)
                    msg.attach(MIMEText(body, 'html'))

                    # In a real scenario, we'd use SSL/TLS
                    # with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
                    #     server.login(self.user, self.password)
                    #     server.send_message(msg)
                    
                    print(f"[*] Simulated send to {target} | Link: {tracking_link}")
                    if callback:
                        callback(campaign_id, 1, 0, 0)
                except Exception as e:
                    print(f"[!] Error sending to {target}: {e}")

        threading.Thread(target=worker, daemon=True).start()
