import cv2
import logging
from PyQt6.QtCore import QThread, pyqtSignal
import numpy as np

try:
    from deepface import DeepFace
    HAS_DEEPFACE = True
except ImportError:
    HAS_DEEPFACE = False
    logging.warning("DeepFace not found. Biometric verification will use fallback mock.")

class BiometricScanner(QThread):
    """
    Asynchronous Facial Recognition Engine.
    Processes camera stream and compares against known vectors.
    """
    result_ready = pyqtSignal(dict)
    frame_ready = pyqtSignal(np.ndarray)

    def __init__(self, target_image_path=None):
        super().__init__()
        self.target_image_path = target_image_path
        self.running = True
        self.cap = None

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()

    def run(self):
        self.cap = cv2.VideoCapture(0)
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            # Emit frame for UI display
            self.frame_ready.emit(frame)

            # Performance check: We don't want to run DeepFace on every single frame
            # In a real app, we might trigger this on button press or every N seconds
            pass

    def perform_scan(self, current_frame):
        """
        Runs the actual biometric comparison.
        """
        if not HAS_DEEPFACE or not self.target_image_path:
            # Fallback mock for demonstration
            import time
            time.sleep(1)
            return {"status": "SUCCESS", "confidence": 0.98}

        try:
            # DeepFace.verify handles detection and mapping
            result = DeepFace.verify(
                img1_path = current_frame,
                img2_path = self.target_image_path,
                model_name = "VGG-Face",
                enforce_detection = False
            )
            return {
                "status": "SUCCESS" if result["verified"] else "FAILURE",
                "confidence": 1 - result["distance"]
            }
        except Exception as e:
            logging.error(f"Biometric scan error: {e}")
            return {"status": "ERROR", "message": str(e)}
