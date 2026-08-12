import sys
import os
import cv2
from PyQt6.QtWidgets import QApplication, QStackedWidget, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt

# Local Imports
from ui.window_manager import FramelessWindow
from ui.views.auth_view import AuthView
from core.biometrics import BiometricScanner
from core.mfa_service import MFAService
from core.crypto_vault import CryptoVault
from utils.logger import ZeroTrustLogger

class ZeroTrustApp(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zero-Trust Identity Suite")
        self.setFixedSize(450, 700)
        
        # System State
        self.logger = ZeroTrustLogger()
        self.mfa = MFAService(secret="JBSWY3DPEHPK3PXP") # Demo Secret
        self.vault = CryptoVault("HSINI_MOHAMED_PRO_2026")
        
        self.init_ui()
        self.load_styles()
        
        # Start Biometrics
        self.scanner = BiometricScanner()
        self.scanner.frame_ready.connect(self.auth_view.update_frame)
        self.scanner.start()

    def init_ui(self):
        self.central_widget = QFrame()
        self.central_widget.setObjectName("MainFrame")
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.stack = QStackedWidget()
        self.auth_view = AuthView()
        self.stack.addWidget(self.auth_view)
        
        self.main_layout.addWidget(self.stack)
        
        # Connect Signals
        self.auth_view.auth_btn.clicked.connect(self.handle_authentication)

    def load_styles(self):
        style_path = os.path.join("ui", "styles", "vault_theme.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())

    def handle_authentication(self):
        self.auth_view.status.setText("VERIFYING TRINITY IDENTITY...")
        self.auth_view.status.setStyleSheet("color: #00F2FF;")
        
        # 1. MFA Verification
        token = self.auth_view.mfa_input.text()
        mfa_valid = self.mfa.verify_token(token)
        
        # 2. Biometric Verification (Mocked for Demo if camera/DeepFace not ready)
        # In real usage, we'd capture the current frame and pass it to scanner.perform_scan()
        bio_result = {"status": "SUCCESS", "confidence": 0.97}
        
        if mfa_valid and bio_result["status"] == "SUCCESS":
            self.auth_view.status.setText("ACCESS GRANTED: WELCOME HSINI")
            self.auth_view.status.setStyleSheet("color: #00FF41;")
            self.logger.log_attempt(0.97, "VALID", "LOGIN_SUCCESS")
        else:
            reason = "MFA_INVALID" if not mfa_valid else "FACE_MISMATCH"
            self.auth_view.status.setText(f"ACCESS DENIED: {reason}")
            self.auth_view.status.setStyleSheet("color: #FF3B30;")
            self.logger.log_attempt(0.0, "INVALID" if not mfa_valid else "VALID", "LOGIN_FAILURE", reason)

    def closeEvent(self, event):
        self.scanner.stop()
        self.scanner.wait()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZeroTrustApp()
    window.show()
    sys.exit(app.exec())
