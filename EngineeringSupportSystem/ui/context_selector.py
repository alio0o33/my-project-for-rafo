# ui/context_selector.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
from base_store import load_bases, aircraft_by_base

class ContextSelector(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Airbase & Aircraft")
        self.resize(420, 200)

        self.base_combo = QComboBox()
        self.aircraft_combo = QComboBox()

        self._populate_bases()

        self.base_combo.currentIndexChanged.connect(self._on_base_change)

        ok_btn = QPushButton("Continue")
        ok_btn.clicked.connect(self.accept)

        layout = QVBoxLayout(self)
        row1 = QHBoxLayout(); row1.addWidget(QLabel("Airbase")); row1.addWidget(self.base_combo)
        row2 = QHBoxLayout(); row2.addWidget(QLabel("Aircraft (Tail)")); row2.addWidget(self.aircraft_combo)

        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addWidget(ok_btn)

    def _populate_bases(self):
        self.bases = load_bases()
        self.base_combo.clear()
        for b in self.bases:
            self.base_combo.addItem(f"{b['name']} ({b['id']})", b["id"])
        if self.bases:
            self._on_base_change(0)

    def _on_base_change(self, _idx: int):
        base_id = self.base_combo.currentData()
        self.aircraft_combo.clear()
        items = aircraft_by_base(base_id)
        for a in items:
            self.aircraft_combo.addItem(f"{a['tail']}  |  {a['model']}", a["tail"])

    def selected_context(self):
        base_id = self.base_combo.currentData()
        tail = self.aircraft_combo.currentData()
        return {"base_id": base_id, "tail": tail}
