# ui/task_editor.py (replace file with this version)
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTextEdit, QComboBox, QPushButton, QMessageBox, QLabel
from data_store import add_task, list_usernames
from base_store import load_bases, aircraft_by_base

class TaskEditorDialog(QDialog):
    def __init__(self, parent=None, context: dict | None = None):
        super().__init__(parent)
        self.setWindowTitle("Create Maintenance Task")
        self.resize(460, 420)
        self.context = context or {}

        # Base & aircraft selectors
        self.base_combo = QComboBox()
        for b in load_bases():
            self.base_combo.addItem(f"{b['name']} ({b['id']})", b["id"])

        self.tail_combo = QComboBox()
        self.base_combo.currentIndexChanged.connect(self._on_base_change)

        # Preselect context
        if self.context.get("base_id"):
            idx = self.base_combo.findData(self.context["base_id"])
            if idx >= 0: self.base_combo.setCurrentIndex(idx)
        self._on_base_change(0)
        if self.context.get("tail"):
            t_idx = self.tail_combo.findData(self.context["tail"])
            if t_idx >= 0: self.tail_combo.setCurrentIndex(t_idx)

        self.title_edit = QLineEdit(); self.title_edit.setPlaceholderText("Task title")
        self.details_edit = QTextEdit(); self.details_edit.setPlaceholderText("Task details / instructions")
        self.assignee_combo = QComboBox(); self.assignee_combo.addItem("(Unassigned)")
        for u in list_usernames(): self.assignee_combo.addItem(u)
        self.status_combo = QComboBox(); self.status_combo.addItems(["pending", "in_progress"])

        create_btn = QPushButton("Create Task"); create_btn.clicked.connect(self._create)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Airbase")); layout.addWidget(self.base_combo)
        layout.addWidget(QLabel("Aircraft (Tail)")); layout.addWidget(self.tail_combo)
        layout.addWidget(QLabel("Title")); layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("Details")); layout.addWidget(self.details_edit)
        layout.addWidget(QLabel("Assign to (optional)")); layout.addWidget(self.assignee_combo)
        layout.addWidget(QLabel("Initial status")); layout.addWidget(self.status_combo)
        layout.addWidget(create_btn)

    def _on_base_change(self, _i):
        base_id = self.base_combo.currentData()
        self.tail_combo.clear()
        for a in aircraft_by_base(base_id):
            self.tail_combo.addItem(f"{a['tail']}  |  {a['model']}", a["tail"])

    def _create(self):
        base_id = self.base_combo.currentData()
        tail = self.tail_combo.currentData()
        title = self.title_edit.text().strip()
        if not title:
            QMessageBox.warning(self, "Required", "Title is required."); return
        details = self.details_edit.toPlainText().strip()
        assigned_to = self.assignee_combo.currentText()
        if assigned_to == "(Unassigned)":
            assigned_to = None
        status = self.status_combo.currentText()

        add_task({
            "title": title,
            "details": details,
            "assigned_to": assigned_to,
            "status": status,
            "base_id": base_id,
            "aircraft_tail": tail
        })
        QMessageBox.information(self, "Created", f"Task created for {base_id} / {tail}")
        self.accept()
