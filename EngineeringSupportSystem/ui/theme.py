# ui/theme.py
from pathlib import Path

ASSETS = Path(__file__).parents[1] / "assets"
ICONS = ASSETS / "icons"

def icon_path(name: str) -> str:
    return str(ICONS / name)

APP_QSS = """
* { font-family: 'Segoe UI', 'Arial'; font-size: 12px; }
QMainWindow { background: #0c1116; }
QLabel#title { color: #e6edf3; font-size: 18px; font-weight: 600; }
QPushButton {
    background: #1f6feb; color: white; border: 0; padding: 8px 12px;
    border-radius: 10px;
}
QPushButton:hover { background: #2b7bff; }
QPushButton:pressed { background: #165bd8; }
QLineEdit, QTextEdit, QComboBox, QListWidget {
    background: #0f1720; color: #dce3ea; border: 1px solid #243040;
    border-radius: 10px; padding: 8px;
}
QListWidget::item { padding: 8px; }
QListWidget::item:selected { background: #1b2636; border-radius: 8px; }
QToolBar {
    background: #0f1621; spacing: 6px; padding: 6px;
    border-bottom: 1px solid #233044;
}
QToolButton { padding: 6px 10px; border-radius: 8px; }
QToolButton:hover { background: #1a2230; }

QLabel#contextChip {
    background: #142031;
    color: #cfe3ff;
    border: 1px solid #2a3a54;
    border-radius: 14px;   /* pill shape */
    padding: 4px 10px;
    font-size: 12px;
}
"""

