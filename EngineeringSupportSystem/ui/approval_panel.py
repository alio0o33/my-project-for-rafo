# ui/approval_panel.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QMessageBox
from data_store import load_tasks, save_tasks

APPROVABLE_STATES = {"completed", "in_review"}

class ApprovalPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.list = QListWidget()
        self.info = QLabel("Completed / In-Review Tasks")
        self.btn_refresh = QPushButton("Refresh")
        self.btn_approve = QPushButton("Approve")
        self.btn_reject = QPushButton("Reject")

        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_approve.clicked.connect(lambda: self._set_status("approved"))
        self.btn_reject.clicked.connect(lambda: self._set_status("rejected"))

        bar = QHBoxLayout()
        bar.addWidget(self.btn_refresh)
        bar.addWidget(self.btn_approve)
        bar.addWidget(self.btn_reject)

        layout = QVBoxLayout(self)
        layout.addWidget(self.info)
        layout.addWidget(self.list)
        layout.addLayout(bar)

        self.refresh()

    def refresh(self):
        self.list.clear()
        for t in load_tasks():
            if t.get("status") in APPROVABLE_STATES:
                self.list.addItem(f"#{t['id']} | {t['title']} | {t['status']} | {t.get('assigned_to') or 'Unassigned'}")

    def _set_status(self, status: str):
        item = self.list.currentItem()
        if not item:
            QMessageBox.warning(self, "Select", "Select a task.")
            return
        tid = int(item.text().split("|")[0].strip().lstrip("#"))
        tasks = load_tasks()
        for t in tasks:
            if t["id"] == tid:
                t["status"] = status
                save_tasks(tasks)
                QMessageBox.information(self, "Updated", f"Task #{tid} → {status}")
                self.refresh()
                return
        QMessageBox.warning(self, "Not Found", "Task not found.")
