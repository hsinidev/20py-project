from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QStackedWidget)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QPen, QImage, QPixmap

class PulseRing(QWidget):
    """
    Animated Cyber-Cyan pulse ring for biometric scan visualization.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(220, 220)
        self._radius = 80
        self._opacity = 1.0
        
        self.anim = QPropertyAnimation(self, b"radius")
        self.anim.setDuration(2000)
        self.anim.setStartValue(80)
        self.anim.setEndValue(100)
        self.anim.setLoopCount(-1)
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim.start()

    @pyqtProperty(int)
    def radius(self): return self._radius
    @radius.setter
    def radius(self, val):
        self._radius = val
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw outer glowing ring
        pen = QPen(QColor(0, 242, 255, 150))
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawEllipse(self.rect().center(), self._radius, self._radius)
        
        # Draw inner core
        painter.setBrush(QColor(0, 242, 255, 30))
        painter.drawEllipse(self.rect().center(), 75, 75)

class AuthView(QWidget):
    """
    The Zero-Trust Authentication View.
    Features: Biometric Feed, Pulse Ring, and MFA Input.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Title
        title = QLabel("IDENTITY VERIFICATION")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Scanner Container
        scan_container = QFrame()
        scan_container.setObjectName("GlassContainer")
        scan_container.setFixedSize(320, 320)
        scan_layout = QVBoxLayout(scan_container)
        
        self.video_feed = QLabel()
        self.video_feed.setFixedSize(280, 280)
        self.video_feed.setStyleSheet("background: black; border-radius: 140px;")
        scan_layout.addWidget(self.video_feed, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.pulse = PulseRing(self.video_feed)
        self.pulse.move(30, 30)
        
        layout.addWidget(scan_container, alignment=Qt.AlignmentFlag.AlignCenter)

        # MFA Input
        self.mfa_input = QLineEdit()
        self.mfa_input.setPlaceholderText("ENTER 6-DIGIT TOTP TOKEN")
        self.mfa_input.setMaxLength(6)
        self.mfa_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.mfa_input)

        # Auth Button
        self.auth_btn = QPushButton("INITIATE TRINITY AUTH")
        self.auth_btn.setObjectName("AuthButton")
        layout.addWidget(self.auth_btn)

        # Status
        self.status = QLabel("SYSTEM READY: STANDBY FOR BIOMETRICS")
        self.status.setObjectName("StatusLabel")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status)

    def update_frame(self, frame):
        """Updates the video feed label with a new OpenCV frame"""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.video_feed.setPixmap(QPixmap.fromImage(qt_image).scaled(280, 280, Qt.AspectRatioMode.KeepAspectRatioByExpanding))
