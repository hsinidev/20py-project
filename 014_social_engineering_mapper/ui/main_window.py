import sys
import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLineEdit, QListWidget, QLabel, 
                             QProgressBar, QGroupBox, QFrame)
from PySide6.QtCore import Qt, Signal, QThread
from ui.web_view import RiskHeatmap

class ScanWorker(QThread):
    progress = Signal(int)
    log = Signal(str)
    finished = Signal(list)

    def __init__(self, targets):
        super().__init__()
        self.targets = targets

    def run(self):
        from scrapers.manager import ScraperManager
        from analysis.nlp_engine import SocialNLP
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        mgr = ScraperManager()
        nlp = SocialNLP()
        results = []

        for i, url in enumerate(self.targets):
            self.log.emit(f"Scraping: {url}...")
            # Simulated departmental assignment for demo
            depts = ["HR", "Finance", "IT", "Sales", "Executive"]
            dept = depts[i % len(depts)]
            
            # Scrape
            raw_data = loop.run_until_complete(mgr.scrape_target(url))
            if raw_data:
                # Analyze
                analysis = nlp.analyze_text(raw_data['content'])
                results.append({
                    "department": dept,
                    "url": url,
                    "nlp_results": analysis
                })
                self.log.emit(f"Analysis Complete: {url} (Risk: {analysis['risk_score']})")
            
            progress_val = int(((i + 1) / len(self.targets)) * 100)
            self.progress.emit(progress_val)
        
        self.finished.emit(results)

class EnterpriseDashboard(QMainWindow):
    """
    Strategic Minimalist Dashboard for Social Engineering Audit.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Social Engineering Vulnerability Mapper v2.1.0")
        self.setMinimumSize(1200, 800)
        
        # UI State
        self.scan_results = []
        
        self.init_ui()
        self.load_styles()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- Left Panel (Controls & Targets) ---
        left_panel = QVBoxLayout()
        
        # Target Input
        input_group = QGroupBox("STRATEGIC TARGETING")
        input_layout = QVBoxLayout(input_group)
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter URL (e.g. linkedin.com/company/...)")
        self.add_btn = QPushButton("ADD TARGET")
        self.add_btn.clicked.connect(self.add_target)
        input_layout.addWidget(self.target_input)
        input_layout.addWidget(self.add_btn)
        
        # Target List
        self.target_list = QListWidget()
        input_layout.addWidget(QLabel("Audit Queue:"))
        input_layout.addWidget(self.target_list)
        
        # Actions
        self.start_btn = QPushButton("INITIATE GLOBAL AUDIT")
        self.start_btn.setFixedHeight(50)
        self.start_btn.clicked.connect(self.start_audit)
        
        self.export_btn = QPushButton("GENERATE EXECUTIVE REPORT")
        self.export_btn.setEnabled(False)
        self.export_btn.clicked.connect(self.export_report)
        
        left_panel.addWidget(input_group)
        left_panel.addWidget(self.start_btn)
        left_panel.addWidget(self.export_btn)
        
        # --- Right Panel (Intelligence & Mapping) ---
        right_panel = QVBoxLayout()
        
        # Risk Matrix Matrix
        matrix_group = QGroupBox("LIVE RISK MATRIX (HEATMAP)")
        matrix_layout = QVBoxLayout(matrix_group)
        self.heatmap = RiskHeatmap()
        matrix_layout.addWidget(self.heatmap)
        
        # Event Log
        log_group = QGroupBox("TACTICAL INTELLIGENCE FEED")
        log_layout = QVBoxLayout(log_group)
        self.event_log = QListWidget()
        log_layout.addWidget(self.event_log)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        
        right_panel.addWidget(matrix_group, 2)
        right_panel.addWidget(log_group, 1)
        right_panel.addWidget(self.progress_bar)

        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 2)

    def load_styles(self):
        style_path = os.path.join(os.path.dirname(__file__), "assets", "theme.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())

    def add_target(self):
        url = self.target_input.text().strip()
        if url:
            self.target_list.addItem(url)
            self.target_input.clear()

    def start_audit(self):
        targets = [self.target_list.item(i).text() for i in range(self.target_list.count())]
        if not targets:
            return

        self.start_btn.setEnabled(False)
        self.export_btn.setEnabled(False)
        self.event_log.clear()
        
        self.worker = ScanWorker(targets)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.log.connect(lambda msg: self.event_log.addItem(f"> {msg}"))
        self.worker.finished.connect(self.on_audit_complete)
        self.worker.start()

    def on_audit_complete(self, results):
        from analysis.risk_matrix import RiskMatrix
        self.scan_results = results
        self.start_btn.setEnabled(True)
        self.export_btn.setEnabled(True)
        
        # Update Matrix
        rm = RiskMatrix()
        matrix = rm.aggregate_data(results)
        heatmap_data = rm.get_heatmap_data()
        self.heatmap.update_heatmap(heatmap_data)
        
        self.event_log.addItem("AUDIT COMPLETE: All tactical data synthesized.")

    def export_report(self):
        from analysis.risk_matrix import RiskMatrix
        from exports.html_generator import ReportGenerator
        
        rm = RiskMatrix()
        matrix = rm.aggregate_data(self.scan_results)
        
        data = {
            "target_org": "Enterprise Audit",
            "overall_risk": matrix["avg_risk"].mean() if not matrix.empty else 0.0,
            "matrix_data": matrix.to_dict(orient="records")
        }
        
        gen = ReportGenerator()
        path = os.path.join("exports", "vulnerability_report.html")
        gen.generate(data, path)
        self.event_log.addItem(f"REPORT GENERATED: {path}")
        os.startfile(path) if sys.platform == 'win32' else None
