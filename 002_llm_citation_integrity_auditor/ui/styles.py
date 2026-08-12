from core.models import THEME

QSS = f"""
QMainWindow {{
    background-color: {THEME['bg']};
}}

QFrame#Sidebar {{
    background-color: {THEME['card']};
    border-right: 1px solid {THEME['border']};
}}

QFrame#Card {{
    background-color: {THEME['card']};
    border: 1px solid {THEME['border']};
    border-radius: 8px;
}}

QLabel#Title {{
    color: {THEME['navy']};
    font-size: 18px;
    font-weight: bold;
}}

QLabel#SubTitle {{
    color: {THEME['slate']};
    font-size: 11px;
}}

QLineEdit, QTextEdit {{
    background-color: {THEME['card']};
    border: 1px solid {THEME['border']};
    border-radius: 6px;
    padding: 8px;
    color: {THEME['navy']};
    font-family: 'Segoe UI', sans-serif;
}}

QLineEdit:focus, QTextEdit:focus {{
    border: 1px solid {THEME['emerald']};
}}

QPushButton {{
    background-color: {THEME['emerald']};
    color: white;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 12px;
}}

QPushButton:hover {{
    background-color: #0d9488;
}}

QPushButton:disabled {{
    background-color: {THEME['border']};
    color: {THEME['slate']};
}}

QProgressBar {{
    border: 1px solid {THEME['border']};
    border-radius: 4px;
    text-align: center;
    background-color: {THEME['emerald_dim']};
}}

QProgressBar::chunk {{
    background-color: {THEME['emerald']};
}}

QTableWidget {{
    background-color: white;
    border: 1px solid {THEME['border']};
    gridline-color: {THEME['border']};
    border-radius: 6px;
}}

QHeaderView::section {{
    background-color: {THEME['bg']};
    padding: 6px;
    border: none;
    border-bottom: 1px solid {THEME['border']};
    color: {THEME['slate']};
    font-weight: bold;
}}

QTabWidget::pane {{
    border: 1px solid {THEME['border']};
    border-radius: 8px;
    background: white;
}}

QTabBar::tab {{
    background: transparent;
    padding: 10px 20px;
    color: {THEME['slate']};
}}

QTabBar::tab:selected {{
    color: {THEME['emerald']};
    border-bottom: 2px solid {THEME['emerald']};
}}
"""
