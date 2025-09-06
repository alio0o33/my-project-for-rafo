# app.py (replace with this minimal update)
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.login_window import LoginWindow
from ui.theme import APP_QSS, ASSETS

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(ASSETS / "app_icon.png")))
    app.setStyleSheet(APP_QSS)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
