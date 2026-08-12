import sys
import threading
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QLineEdit, QTextEdit, QTableWidget, 
                             QTableWidgetItem, QStackedWidget, QFrame, QMessageBox, QSplashScreen)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QColor, QPalette, QPixmap

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

# Core Logic Imports
from core.database import EncryptedVault
from core.server import run_server
from core.mailer import MailEngine
from core.reporter import AuditReporter

class StatsObserver(QObject):
    update_signal = pyqtSignal()
    
    def log_click(self, cid):
        print(f"[*] Click logged for campaign {cid}")
        self.vault.update_stats(cid, click=1)
        self.update_signal.emit()

    def log_compromised(self, cid):
        print(f"[*] Compromise logged for campaign {cid}")
        self.vault.update_stats(cid, compromised=1)
        self.update_signal.emit()

    def set_vault(self, vault):
        self.vault = vault

class MainWindow(QMainWindow):
    def __init__(self, observer):
        super().__init__()
        self.observer = observer
        self.vault = EncryptedVault()
        self.observer.set_vault(self.vault)
        
        self.setWindowTitle("Automated Phishing Campaign Simulator | Corporate Audit v1.0")
        self.resize(1200, 800)
        
        # Theme Colors
        self.navy = "#001f3f"
        self.white = "#FFFFFF"
        self.grey = "#F8F9FA"
        
        self.setup_ui()
        
        # Refresh Timer
        self.observer.update_signal.connect(self.refresh_dashboard)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet(f"background-color: {self.navy}; color: white; border: none;")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 40, 20, 20)

        logo = QLabel("AUDIT CORE")
        logo.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        logo.setStyleSheet("margin-bottom: 30px;")
        sidebar_layout.addWidget(logo)

        nav_btns = [("Dashboard", 0), ("Campaign Builder", 1), ("Target Lists", 2), ("Audit Reports", 3)]
        self.btns = []
        for text, index in nav_btns:
            btn = QPushButton(text)
            btn.setFlat(True)
            btn.setStyleSheet("text-align: left; padding: 10px; font-size: 14px; border-radius: 5px;")
            btn.clicked.connect(lambda checked, idx=index: self.stack.setCurrentIndex(idx))
            sidebar_layout.addWidget(btn)
            self.btns.append(btn)

        sidebar_layout.addStretch()
        
        status_lbl = QLabel("SYSTEM STATUS: ACTIVE")
        status_lbl.setStyleSheet("color: #00FF00; font-size: 10px;")
        sidebar_layout.addWidget(status_lbl)

        main_layout.addWidget(self.sidebar)

        # Content Area
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background-color: {self.white};")
        
        self.view_dashboard = self._create_dashboard()
        self.view_builder = self._create_builder()
        self.view_targets = self._create_placeholder("Target List Management")
        self.view_reports = self._create_placeholder("Generated Audit Reports")
        
        self.stack.addWidget(self.view_dashboard)
        self.stack.addWidget(self.view_builder)
        self.stack.addWidget(self.view_targets)
        self.stack.addWidget(self.view_reports)

        main_layout.addWidget(self.stack)

    def _create_dashboard(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        header = QLabel("Campaign Analytics Overview")
        header.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {self.navy};")
        layout.addWidget(header)

        # Stats Cards
        stats_layout = QHBoxLayout()
        self.card_sent = self._create_stat_card("Total Sent", "0")
        self.card_clicks = self._create_stat_card("Total Clicks", "0")
        self.card_risk = self._create_stat_card("Risk Level", "LOW")
        stats_layout.addWidget(self.card_sent)
        stats_layout.addWidget(self.card_clicks)
        stats_layout.addWidget(self.card_risk)
        layout.addLayout(stats_layout)

        # Chart
        self.figure, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        refresh_btn = QPushButton("Refresh Analytics")
        refresh_btn.setStyleSheet(f"background-color: {self.navy}; color: white; padding: 10px; border-radius: 5px;")
        refresh_btn.clicked.connect(self.refresh_dashboard)
        layout.addWidget(refresh_btn)

        return page

    def _create_stat_card(self, title, val):
        card = QFrame()
        card.setStyleSheet("background-color: #F0F2F5; border-radius: 10px; border: 1px solid #E0E0E0;")
        layout = QVBoxLayout(card)
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("color: #666; font-size: 12px;")
        v_lbl = QLabel(val)
        v_lbl.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        v_lbl.setStyleSheet(f"color: {self.navy};")
        layout.addWidget(t_lbl)
        layout.addWidget(v_lbl)
        
        # Store label for updates
        if title == "Total Sent": self.lbl_sent = v_lbl
        if title == "Total Clicks": self.lbl_clicks = v_lbl
        if title == "Risk Level": self.lbl_risk = v_lbl
        
        return card

    def _create_builder(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        layout.addWidget(QLabel("Configure New Phishing Simulation", font=QFont("Segoe UI", 22, QFont.Weight.Bold)))
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Campaign Name (e.g., Q3 Security Audit)")
        layout.addWidget(self.name_input)

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Email Subject")
        layout.addWidget(self.subject_input)

        self.targets_input = QTextEdit()
        self.targets_input.setPlaceholderText("Target Emails (one per line)")
        layout.addWidget(self.targets_input)

        self.template_input = QTextEdit()
        self.template_input.setPlaceholderText("HTML Email Body (Use {{LINK}} for tracking)")
        self.template_input.setText("<h3>Important Security Update</h3><p>Your account requires verification. Please <a href='{{LINK}}'>click here</a> to proceed.</p>")
        layout.addWidget(self.template_input)

        launch_btn = QPushButton("Launch Simulation Campaign")
        launch_btn.setStyleSheet(f"background-color: #D9534F; color: white; padding: 15px; font-weight: bold; border-radius: 5px;")
        launch_btn.clicked.connect(self.launch_campaign)
        layout.addWidget(launch_btn)

        return page

    def _create_placeholder(self, text):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel(text, font=QFont("Segoe UI", 18)))
        if text == "Generated Audit Reports":
            btn = QPushButton("Generate Latest Report (PDF)")
            btn.clicked.connect(self.generate_pdf)
            layout.addWidget(btn)
        return page

    def refresh_dashboard(self):
        campaigns = self.vault.get_campaigns()
        if not campaigns: return
        
        total_sent = sum(c[3] for c in campaigns)
        total_clicks = sum(c[4] for c in campaigns)
        total_compromised = sum(c[5] for c in campaigns)
        
        self.lbl_sent.setText(str(total_sent))
        self.lbl_clicks.setText(str(total_clicks))
        self.lbl_risk.setText("HIGH" if total_compromised > 0 else "LOW")
        
        # Update Chart
        self.ax.clear()
        labels = ['Sent', 'Clicked', 'Compromised']
        values = [total_sent, total_clicks, total_compromised]
        self.ax.bar(labels, values, color=[self.navy, '#FF8C00', '#D9534F'])
        self.ax.set_title("Global Campaign Performance")
        self.canvas.draw()

    def launch_campaign(self):
        name = self.name_input.text()
        subject = self.subject_input.text()
        targets = self.targets_input.toPlainText().strip().split('\n')
        body = self.template_input.toPlainText()

        if not name or not targets:
            QMessageBox.warning(self, "Error", "Campaign name and targets are required.")
            return

        self.vault.save_campaign(name, {"subject": subject, "body": body})
        campaigns = self.vault.get_campaigns()
        cid = campaigns[-1][0]

        # Simulate sending
        engine = MailEngine("smtp.example.com", 587, "audit@corp.com", "pass")
        engine.send_campaign(cid, targets, subject, body, self.vault.update_stats)
        
        QMessageBox.information(self, "Success", f"Campaign '{name}' launched successfully in simulation mode.")
        self.stack.setCurrentIndex(0)
        self.refresh_dashboard()

    def generate_pdf(self):
        campaigns = self.vault.get_campaigns()
        if not campaigns: return
        latest = campaigns[-1]
        stats = {'sent': latest[3], 'clicks': latest[4], 'compromised': latest[5]}
        path = AuditReporter.generate_report(latest[1], stats)
        QMessageBox.information(self, "Report Generated", f"PDF Report saved to {path}")

def show_splash():
    splash_pix = QPixmap(600, 400)
    splash_pix.fill(QColor("#001f3f"))
    splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)
    
    label = QLabel("AUTHORIZIED USE ONLY", splash)
    label.setStyleSheet("color: white; font-weight: bold; font-size: 24px;")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setGeometry(0, 150, 600, 50)
    
    sub_label = QLabel("This software is for organizational security auditing purposes.\nUnauthorized use is strictly prohibited.", splash)
    sub_label.setStyleSheet("color: #A8A8A8; font-size: 14px;")
    sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    sub_label.setGeometry(0, 200, 600, 60)

    splash.show()
    return splash

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    splash = show_splash()
    time.sleep(2) # Show splash for 2 seconds
    
    observer = StatsObserver()
    
    # Run Flask in background
    threading.Thread(target=run_server, args=(5000, observer), daemon=True).start()
    
    window = MainWindow(observer)
    splash.finish(window)
    window.show()
    sys.exit(app.exec())
