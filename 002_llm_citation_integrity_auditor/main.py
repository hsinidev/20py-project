import sys
import asyncio
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit, 
                             QPushButton, QFrame, QProgressBar, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QTabWidget, QScrollArea)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QIcon

from core.models import THEME, GroundingLevel, AuditResult
from core.auditor import CitationAuditor
from core.similarity import SimilarityEngine
from ui.styles import QSS

class AuditWorker(QThread):
    finished = pyqtSignal(object)
    log = pyqtSignal(str)

    def __init__(self, query, response):
        super().__init__()
        self.query = query
        self.response = response

    def run(self):
        auditor = CitationAuditor()
        # Run async audit in a loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(auditor.audit(self.query, self.response))
        self.finished.emit(result)

class CitationAuditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLM Citation Integrity Auditor | HSINI MOHAMED")
        self.resize(1400, 900)
        self.setStyleSheet(QSS)
        
        self.init_ui()
        self.log("System Ready. Load source text to begin grounding analysis.")
        
        import threading
        threading.Thread(target=self._load_model, daemon=True).start()

    def _load_model(self):
        if SimilarityEngine.load():
            self.log("✓ Semantic Engine loaded successfully.")
        else:
            self.log("⚠ Semantic Engine: Falling back to Jaccard similarity.")

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # -- Sidebar ----------------------------------------------------------
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(320)
        s_layout = QVBoxLayout(sidebar)
        
        logo = QLabel("🔬")
        logo.setFont(QFont("Segoe UI", 32))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        s_layout.addWidget(logo)

        title = QLabel("CITATION AUDITOR")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        s_layout.addWidget(title)
        
        subtitle = QLabel("LLM TRUTH-GROUNDING LAB")
        subtitle.setObjectName("SubTitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        s_layout.addWidget(subtitle)
        
        s_layout.addSpacing(30)
        
        s_layout.addWidget(QLabel("Audit Query:"))
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter search query...")
        s_layout.addWidget(self.query_input)
        
        s_layout.addSpacing(15)
        
        s_layout.addWidget(QLabel("LLM Response to Audit:"))
        self.response_input = QTextEdit()
        self.response_input.setPlaceholderText("Paste LLM response with citations here...")
        self.response_input.setText("The Earth is roughly 4.54 billion years old [1]. It is the third planet from the Sun [2].\n\n[1]: https://en.wikipedia.org/wiki/Age_of_the_Earth\n[2]: https://en.wikipedia.org/wiki/Earth")
        s_layout.addWidget(self.response_input)
        
        s_layout.addSpacing(20)
        
        self.run_btn = QPushButton("EXECUTE AUDIT")
        self.run_btn.clicked.connect(self.start_audit)
        s_layout.addWidget(self.run_btn)
        
        s_layout.addStretch()
        
        footer = QLabel("Developed by HSINI MOHAMED")
        footer.setObjectName("SubTitle")
        s_layout.addWidget(footer)

        # -- Content Area -----------------------------------------------------
        content = QWidget()
        c_layout = QVBoxLayout(content)
        c_layout.setContentsMargins(25, 25, 25, 25)
        c_layout.setSpacing(20)

        # Top Stats Row
        stats_row = QHBoxLayout()
        self.score_card = self.create_stat_card("GROUNDING SCORE", "0%", THEME["emerald"])
        self.claims_card = self.create_stat_card("CLAIMS ANALYZED", "0", THEME["navy"])
        self.status_card = self.create_stat_card("OVERALL STATUS", "PENDING", THEME["slate"])
        
        stats_row.addWidget(self.score_card)
        stats_row.addWidget(self.claims_card)
        stats_row.addWidget(self.status_card)
        c_layout.addLayout(stats_row)

        # Tabs
        self.tabs = QTabWidget()
        c_layout.addWidget(self.tabs)

        # Tab 1: Findings Grid
        self.grid_tab = QWidget()
        gt_layout = QVBoxLayout(self.grid_tab)
        
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Claim Text", "Source URL", "Semantic Score", "Status", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.table.setColumnWidth(0, 400)
        gt_layout.addWidget(self.table)
        
        self.tabs.addTab(self.grid_tab, "🔍 Detailed Findings")

        # Tab 2: System Log
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background: #0f172a; color: #10b981; font-family: 'Consolas';")
        self.tabs.addTab(self.log_output, "📋 System Log")

        layout.addWidget(sidebar)
        layout.addWidget(content)

    def create_stat_card(self, title, val, color):
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedHeight(120)
        l = QVBoxLayout(card)
        t = QLabel(title)
        t.setStyleSheet(f"color: {THEME['slate']}; font-size: 10px; font-weight: bold;")
        v = QLabel(val)
        v.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")
        l.addWidget(t)
        l.addWidget(v)
        card.setProperty("val_label", v)
        return card

    def log(self, msg):
        self.log_output.append(f"[{sys.platform.upper()}] {msg}")
        self.statusBar().showMessage(msg, 5000)

    def start_audit(self):
        query = self.query_input.text()
        response = self.response_input.toPlainText()
        
        if not response.strip():
            self.log("Error: Response text cannot be empty.")
            return
            
        self.run_btn.setEnabled(False)
        self.run_btn.setText("AUDITING...")
        self.log(f"Starting audit for {len(response)} chars of text...")
        
        self.worker = AuditWorker(query, response)
        self.worker.finished.connect(self.on_audit_finished)
        self.worker.start()

    def on_audit_finished(self, result: AuditResult):
        self.run_btn.setEnabled(True)
        self.run_btn.setText("EXECUTE AUDIT")
        self.log(f"Audit completed. Score: {result.overall_score:.1f}%")
        
        # Update Cards
        self.score_card.property("val_label").setText(f"{result.overall_score:.1f}%")
        self.claims_card.property("val_label").setText(str(len(result.claims)))
        
        status = "HEALTHY" if result.overall_score > 80 else "CRITICAL" if result.overall_score < 40 else "UNSTABLE"
        color = THEME["emerald"] if status=="HEALTHY" else THEME["red"] if status=="CRITICAL" else THEME["yellow"]
        self.status_card.property("val_label").setText(status)
        self.status_card.property("val_label").setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")

        # Update Table
        self.table.setRowCount(0)
        for i, claim in enumerate(result.claims):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(claim.text[:100] + "..."))
            self.table.setItem(i, 1, QTableWidgetItem(claim.citations[0].url if claim.citations else "N/A"))
            
            score_item = QTableWidgetItem(f"{claim.grounding_score:.2f}")
            score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 2, score_item)
            
            status_item = QTableWidgetItem(claim.status.value)
            color = THEME["emerald"] if claim.status == GroundingLevel.VERIFIED else THEME["red"] if claim.status == GroundingLevel.HALLUCINATION else THEME["yellow"]
            status_item.setForeground(QColor(color))
            self.table.setItem(i, 3, status_item)
            
            btn = QPushButton("View Diff")
            btn.setFixedSize(80, 25)
            btn.setStyleSheet("background: #64748b; font-size: 10px; padding: 2px;")
            self.table.setCellWidget(i, 4, btn)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CitationAuditorApp()
    window.show()
    sys.exit(app.exec())
