from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGraphicsBlurEffect
from PyQt6.QtCore import Qt, QPoint

class FramelessWindow(QMainWindow):
    """
    Base class for frameless, draggable, and glassmorphic windows.
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.oldPos = self.pos()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()

    def apply_blur(self, widget, radius=20):
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(radius)
        widget.setGraphicsEffect(blur)
