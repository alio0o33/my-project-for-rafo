# ui/training_panel.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QLineEdit, QPushButton, QMessageBox, QComboBox
from training_store import load_training, add_session, assign_user, set_assignment_status
from data_store import list_usernames

class TrainingPanel(QWidget):
    def __init__(self, current_user: str = "", role: str = ""):
        super().__init__()
        self.current_user = current_user
        self.role = role

        # Sessions
        self.sessions = QListWidget()
        self.assignments = QListWidget()

        # Create session controls (for trainingcoordinator/admin/manager)
        self.title = QLineEdit(); self.title.setPlaceholderText("Session Title")
        self.date = QLineEdit(); self.date.setPlaceholderText("Date (YYYY-MM-DD)")
        create_btn = QPushButton("Create Session")
        create_btn.clicked.connect(self._create_session)

        # Assign user to session
        self.user_combo = QComboBox(); self.user_combo.addItems(list_usernames())
        self.assign_btn = QPushButton("Assign User to Selected Session")
        self.assign_btn.clicked.connect(self._assign_user)

        # Mark complete
        self.mark_complete = QPushButton("Mark Selected Assignment Completed")
        self.mark_complete.clicked.connect(self._complete_assignment)

        top = QHBoxLayout()
        top.addWidget(self.title); top.addWidget(self.date); top.addWidget(create_btn)

        assign_bar = QHBoxLayout()
        assign_bar.addWidget(self.user_combo); assign_bar.addWidget(self.assign_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Training Sessions"))
        layout.addWidget(self.sessions)
        layout.addLayout(top)
        layout.addWidget(QLabel("Assignments"))
        layout.addWidget(self.assignments)
        layout.addLayout(assign_bar)
        layout.addWidget(self.mark_complete)

        self.refresh()

    def refresh(self):
        data = load_training()
        self.sessions.clear()
        for s in data["sessions"]:
            self.sessions.addItem(f"{s['id']} | {s['title']} | {s['date']}")
        self.assignments.clear()
        for a in data["assignments"]:
            self.assignments.addItem(f"{a['user']} | session={a['session_id']} | {a['status']}")

    def _selected_session_id(self):
        item = self.sessions.currentItem()
        if not item: return None
        try:
            return int(item.text().split("|")[0].strip())
        except Exception:
            return None

    def _create_session(self):
        sid = add_session(self.title.text().strip(), self.date.text().strip())
        QMessageBox.information(self, "Created", f"Session #{sid['id']} created.")
        self.title.clear(); self.date.clear()
        self.refresh()

    def _assign_user(self):
        sid = self._selected_session_id()
        if not sid:
            QMessageBox.warning(self, "Select", "Select a session in the top list.")
            return
        user = self.user_combo.currentText()
        if assign_user(user, sid):
            QMessageBox.information(self, "Assigned", f"{user} assigned to session #{sid}.")
            self.refresh()
        else:
            QMessageBox.warning(self, "Error", "Session not found.")

    def _complete_assignment(self):
        item = self.assignments.currentItem()
        if not item:
            QMessageBox.warning(self, "Select", "Select an assignment.")
            return
        parts = [x.strip() for x in item.text().split("|")]
        user = parts[0]
        sid = int(parts[1].split("=")[1])
        if set_assignment_status(user, sid, "completed"):
            QMessageBox.information(self, "Updated", "Marked completed.")
            self.refresh()
        else:
            QMessageBox.warning(self, "Error", "Could not update.")
