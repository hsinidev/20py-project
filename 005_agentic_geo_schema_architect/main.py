import sys
import requests
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
                             QPushButton, QFrame, QScrollArea)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QIcon

from ui.editor import CodeEditor
from core.crawler import AdvancedCrawler
from core.architect import SchemaArchitect

class ArchitectWorker(QThread):
    finished = Signal(dict)
    log = Signal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            self.log.emit("🔍 Deep Crawling Page Assets...")
            crawler = AdvancedCrawler()
            crawl_data = crawler.crawl(self.url)

            if "error" in crawl_data:
                self.finished.emit({"error": crawl_data["error"]})
                return

            self.log.emit("🤖 Architecting High-Fidelity Schema...")
            architect = SchemaArchitect()
            schema = architect.generate_json_ld(self.url, crawl_data)

            self.finished.emit(schema)
        except Exception as e:
            self.finished.emit({"error": str(e)})

class SchemaArchitectApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AGENTIC GEO-SCHEMA ARCHITECT | HSINI MOHAMED")
        self.resize(1200, 800)
        self.setStyleSheet("background-color: #0f0f0f; color: #e0e0e0;")

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        top_bar = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter target URL (e.g., https://example.com)")
        self.url_input.setStyleSheet("""
            QLineEdit { background-color: #1a1a1a; border: 1px solid #333; padding: 10px; border-radius: 5px; font-size: 14px; }
        """)
        
        self.build_btn = QPushButton("EXECUTE ARCHITECT")
        self.build_btn.clicked.connect(self.start_workflow)
        self.build_btn.setStyleSheet("""
            QPushButton { background-color: #b39ddb; color: #1a1a1a; font-weight: bold; padding: 10px 20px; border-radius: 5px; }
            QPushButton:hover { background-color: #d1c4e9; }
        """)
        
        top_bar.addWidget(self.url_input)
        top_bar.addWidget(self.build_btn)
        layout.addLayout(top_bar)

        content = QHBoxLayout()
        bento_scroll = QScrollArea()
        bento_scroll.setWidgetResizable(True)
        bento_scroll.setFixedWidth(300)
        bento_scroll.setStyleSheet("border: none; background: transparent;")
        
        bento_widget = QWidget()
        self.bento_layout = QGridLayout(bento_widget)
        self.bento_layout.setSpacing(10)
        
        self.add_bento_item(0, 0, "ENGINE", "Deep-Scan v2", "#1e1e2e")
        self.add_bento_item(0, 1, "COMPLIANCE", "100%", "#182218")
        self.add_bento_item(1, 0, "ASSET DETECTION", "ENABLED", "#221822")
        self.add_bento_item(1, 1, "STATUS", "IDLE", "#1a1a1a", tag="status_label")
        
        bento_scroll.setWidget(bento_widget)
        content.addWidget(bento_scroll)

        self.editor = CodeEditor()
        content.addWidget(self.editor)
        layout.addLayout(content)

        self.status_bar = QLabel("Developed by HSINI MOHAMED | Professional Auditor Ready")
        self.status_bar.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(self.status_bar)

    def add_bento_item(self, r, c, title, value, color, tag=None):
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {color}; border-radius: 10px; border: 1px solid #333;")
        vbox = QVBoxLayout(frame)
        t_label = QLabel(title)
        t_label.setStyleSheet("color: #888; font-size: 10px; font-weight: bold;")
        v_label = QLabel(value)
        v_label.setStyleSheet("color: #e0e0e0; font-size: 16px; font-weight: bold;")
        if tag: setattr(self, tag, v_label)
        vbox.addWidget(t_label)
        vbox.addWidget(v_label)
        self.bento_layout.addWidget(frame, r, c)

    def start_workflow(self):
        url = self.url_input.text()
        if not url: return
        self.build_btn.setEnabled(False)
        self.status_label.setText("SCANNING")
        self.worker = ArchitectWorker(url)
        self.worker.log.connect(lambda m: self.status_bar.setText(m))
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, schema):
        self.editor.set_json(schema)
        self.build_btn.setEnabled(True)
        self.status_label.setText("DONE")
        self.status_bar.setText("Audit Complete. High-Fidelity Schema Synchronized.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchemaArchitectApp()
    window.show()
    sys.exit(app.exec())
