import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import EnterpriseDashboard
import logging

def main():
    # Fix for GPU/DirectComposition errors on some Windows systems
    import os
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu"

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    app = QApplication(sys.argv)
    
    # Apply global tactical theme
    window = EnterpriseDashboard()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
