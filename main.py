import sys
from PyQt6.QtWidgets import QApplication
from controller import RollerController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    with open("theme.qss", "r") as f:
        app.setStyleSheet(f.read())

    controller = RollerController()
    controller.run()
    
    sys.exit(app.exec())