# ui/manage_users.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QLineEdit, QComboBox, QPushButton, QMessageBox, QLabel
from data_store import load_users, add_user, delete_user
from models import Role

ALL_ROLES: list[Role] = [
    "admin","engineer","supervisor","inspector","technician","planner",
    "qualitycontrol","manager","viewer","scheduler","safetyofficer","logistics",
    "inventorymanager","documentation","trainingcoordinator","flightops",
    "complianceofficer","dataanalyst","helpdesk"
]

class ManageUsersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Users")
        self.resize(520, 420)

        self.list = QListWidget()
        self._refresh()

        self.username = QLineEdit(); self.username.setPlaceholderText("Username")
        self.password = QLineEdit(); self.password.setPlaceholderText("Password")
        self.role = QComboBox(); self.role.addItems(ALL_ROLES)

        add_btn = QPushButton("Add User")
        add_btn.clicked.connect(self._add)
        del_btn = QPushButton("Delete Selected")
        del_btn.clicked.connect(self._delete)

        form = QVBoxLayout()
        form.addWidget(QLabel("Add New User"))
        form.addWidget(self.username)
        form.addWidget(self.password)
        form.addWidget(self.role)
        form.addWidget(add_btn)
        form.addWidget(del_btn)

        layout = QHBoxLayout(self)
        layout.addWidget(self.list, 2)
        layout.addLayout(form, 1)

    def _refresh(self):
        self.list.clear()
        for u in load_users():
            self.list.addItem(f"{u['username']}  |  {u['role']}")

    def _add(self):
        u = self.username.text().strip()
        p = self.password.text().strip()
        r = self.role.currentText()
        if not u or not p:
            QMessageBox.warning(self, "Required", "Username and password are required.")
            return
        if add_user(u, p, r):
            QMessageBox.information(self, "Added", f"User '{u}' created.")
            self.username.clear(); self.password.clear()
            self._refresh()
        else:
            QMessageBox.warning(self, "Exists", f"User '{u}' already exists.")

    def _delete(self):
        item = self.list.currentItem()
        if not item:
            QMessageBox.warning(self, "Select", "Select a user to delete.")
            return
        username = item.text().split("|")[0].strip()
        if username == "admin1":
            QMessageBox.warning(self, "Protected", "Refusing to delete default admin.")
            return
        if delete_user(username):
            QMessageBox.information(self, "Deleted", f"User '{username}' deleted.")
            self._refresh()
        else:
            QMessageBox.warning(self, "Error", "Could not delete user.")
