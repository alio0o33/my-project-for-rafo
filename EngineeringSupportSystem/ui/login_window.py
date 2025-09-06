# ui/login_window.py (drop-in replacement)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from pathlib import Path
from auth import authenticate
from ui.dashboards import DashboardWindow
from ui.context_selector import ContextSelector
from ui.theme import ASSETS

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aircraft Maintenance System - Login")
        self.resize(900, 600)
        self._pixmap = None
        self._init_bg()
        self._init_ui()

    # Wallpaper that scales (no CSS background-size errors)
    def _init_bg(self):
        img = ASSETS / "aircraft.jpg"
        if img.exists():
            self._pixmap = QPixmap(str(img))
            self.setAutoFillBackground(True)
            self._apply_bg()

    def _apply_bg(self):
        if self._pixmap:
            scaled = self._pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            pal = self.palette()
            pal.setBrush(self.backgroundRole(), QBrush(scaled))
            self.setPalette(pal)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._apply_bg()

    def _init_ui(self):
        # Center glass card
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("glassCard")
        card.setStyleSheet("""
            QFrame#glassCard {
                background: rgba(10, 15, 20, 0.65);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 18px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 32, 40, 36)
        card_layout.setSpacing(12)

        # subtle shadow
        shadow = QGraphicsDropShadowEffect(blurRadius=40, xOffset=0, yOffset=12)
        shadow.setColor(Qt.black)
        card.setGraphicsEffect(shadow)

        title = QLabel("Login to Aircraft Maintenance System")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        self.username = QLineEdit(); self.username.setPlaceholderText("Username")
        self.password = QLineEdit(); self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        btn = QPushButton("Sign in")
        btn.clicked.connect(self._on_login)

        for w in (title, self.username, self.password, btn):
            card_layout.addWidget(w)

        # center the card nicely
        root.addStretch(1)
        row = QVBoxLayout()
        row.addWidget(card, alignment=Qt.AlignHCenter)
        root.addLayout(row)
        root.addStretch(2)

    def _on_login(self):
        u = self.username.text().strip()
        p = self.password.text().strip()
        user = authenticate(u, p)
        if not user:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
            return
        role = user.get("role", "engineer")
        # pick base/aircraft
        dlg = ContextSelector(self)
        if not dlg.exec_():
            return
        ctx = dlg.selected_context()
        self.dashboard = DashboardWindow(username=u, role=role, context=ctx)
        self.dashboard.show()
        self.close()
