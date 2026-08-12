from PySide6.QtWidgets import QTextEdit, QWidget, QVBoxLayout
from PySide6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor
from PySide6.QtCore import Qt, QRegularExpression
import json

class JSONHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []

        # Keywords (@type, @context)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#b39ddb")) # Lavender
        keyword_format.setFontWeight(QFont.Bold)
        self.rules.append((QRegularExpression(r'"@\w+"'), keyword_format))

        # Keys
        key_format = QTextCharFormat()
        key_format.setForeground(QColor("#80cbc4")) # Teal
        self.rules.append((QRegularExpression(r'"\w+"(?=\s*:)'), key_format))

        # Values (Strings)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#ce93d8")) # Muted Pink
        self.rules.append((QRegularExpression(r':\s*"(?:\\"|[^"])*"'), string_format))

    def highlightBlock(self, text):
        for expression, format in self.rules:
            iterator = expression.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class CodeEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Consolas", 11))
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #e0e0e0;
                border: 1px solid #333;
                border-radius: 4px;
            }
        """)
        self.highlighter = JSONHighlighter(self.document())

    def set_json(self, data):
        self.setPlainText(json.dumps(data, indent=4))
