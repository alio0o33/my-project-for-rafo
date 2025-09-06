# ui/assign_task.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QMessageBox, QLabel
from data_store import list_usernames, update_task

class AssignTaskDialog(QDialog):
    def __init__(self, task_id: int, current_assignee: str = None, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.setWindowTitle(f"Assign Task #{task_id}")
        self.resize(360, 180)

        self.user_combo = QComboBox()
        self.user_combo.addItems(list_usernames())
        if current_assignee:
            idx = self.user_combo.findText(current_assignee)
            if idx >= 0:
                self.user_combo.setCurrentIndex(idx)

        assign_btn = QPushButton("Assign")
        assign_btn.clicked.connect(self._assign)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Assign to"))
        layout.addWidget(self.user_combo)
        layout.addWidget(assign_btn)

    def _assign(self):
        user = self.user_combo.currentText()
        if not user:
            QMessageBox.warning(self, "Required", "Select a user.")
            return
        ok = update_task(self.task_id, {"assigned_to": user, "status": "in_progress"})
        if not ok:
            QMessageBox.warning(self, "Error", "Task not found.")
            return
        QMessageBox.information(self, "Updated", f"Task #{self.task_id} assigned to {user}.")
        self.accept()
