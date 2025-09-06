from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from data_store import filter_tasks
from inventory_store import low_stock
from training_store import load_training

class SummaryCards(QWidget):
    def __init__(self, context: dict, username: str, role: str):
        super().__init__()
        self.context = context or {}
        self.username = username
        self.role = role
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(0, 0, 0, 12)

        # Build 4 cards
        self.pending = self._make_card("Pending Orders", "0")
        self.completed = self._make_card("Completed Today", "0")
        self.lowstock = self._make_card("Low Stock Items", "0")
        self.training = self._make_card("Upcoming Training", "0")

        for card in (self.pending, self.completed, self.lowstock, self.training):
            self.layout.addWidget(card)

        self.refresh()

    def _make_card(self, title: str, value: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: rgba(20, 30, 45, 0.8);
                border-radius: 16px;
                padding: 12px;
            }
        """)
        v = QVBoxLayout(card)
        label = QLabel(title)
        label.setStyleSheet("color: #9aa4b2; font-size: 12px;")
        val = QLabel(value)
        val.setFont(QFont("Segoe UI", 20, QFont.Bold))
        val.setAlignment(Qt.AlignCenter)
        val.setStyleSheet("color: white;")
        v.addWidget(label)
        v.addWidget(val)
        card.value_label = val
        return card

    def refresh(self):
        base = self.context.get("base_id")
        tail = self.context.get("tail")

        tasks = filter_tasks(base_id=base, aircraft_tail=tail)
        pending_count = sum(1 for t in tasks if t.get("status") in ("pending", "in_progress"))
        completed_today = sum(1 for t in tasks if t.get("status") == "completed")  # simple version

        self.pending.value_label.setText(str(pending_count))
        self.completed.value_label.setText(str(completed_today))

        lows = low_stock()
        self.lowstock.value_label.setText(str(len(lows)))

        training = load_training()
        self.training.value_label.setText(str(len(training.get("sessions", []))))
