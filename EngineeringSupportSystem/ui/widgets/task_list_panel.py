# ui/widgets/task_list_panel.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox, QHBoxLayout, QListWidgetItem
from PyQt5.QtGui import QPixmap, QPainter, QColor, QIcon
from PyQt5.QtCore import QSize
from data_store import load_tasks, save_tasks, filter_tasks

STATUS_COLORS = {
    "pending":      "#9aa4b2",
    "in_progress":  "#2aa3ff",
    "completed":    "#17c964",
    "in_review":    "#f5a524",
    "approved":     "#22c55e",
    "rejected":     "#ef4444",
}

def _dot(color_hex: str, size: int = 14) -> QIcon:
    """Return a small colored dot icon."""
    pm = QPixmap(size, size)
    pm.fill(QColor(0, 0, 0, 0))
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    c = QColor(color_hex)
    p.setBrush(c)
    p.setPen(c.darker(130))
    p.drawEllipse(1, 1, size - 2, size - 2)
    p.end()
    return QIcon(pm)

class TaskListPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.list = QListWidget()
        self.list.setIconSize(QSize(14, 14))

        self.info = QLabel("Select an action to load tasks.")
        self.btn_refresh = QPushButton("Refresh")
        self.btn_mark = QPushButton("Mark Completed")
        self.btn_assign = QPushButton("Assign/Reassign")

        self.btn_refresh.clicked.connect(lambda: self.show_tasks(self._last_mode, self._last_user, self._last_role, self._context))
        self.btn_mark.clicked.connect(lambda: self.mark_selected_complete())
        self.btn_assign.clicked.connect(self._assign_hook)  # hooked by Dashboard

        bar = QHBoxLayout()
        bar.addWidget(self.btn_refresh)
        bar.addWidget(self.btn_mark)
        bar.addWidget(self.btn_assign)

        layout = QVBoxLayout(self)
        layout.addWidget(self.info)
        layout.addWidget(self.list)
        layout.addLayout(bar)

        self._last_mode = "view_my_tasks"
        self._last_user = None
        self._last_role = None
        self._context = {"base_id": None, "tail": None}
        self._perms = {"can_assign": False, "can_mark_complete": True}

        # this is filled by Dashboard, to open Assign dialog
        self._assign_dialog_opener = None

    def set_context(self, ctx: dict):
        self._context = ctx

    def set_permissions(self, perms: dict):
        """perms keys: can_assign, can_mark_complete"""
        self._perms.update(perms or {})
        self.btn_assign.setVisible(bool(self._perms.get("can_assign", False)))
        self.btn_mark.setVisible(bool(self._perms.get("can_mark_complete", True)))

    def set_assign_dialog_opener(self, opener_callable):
        """Dashboard provides a function (task_id, current_assignee) -> open dialog"""
        self._assign_dialog_opener = opener_callable

    def _assign_hook(self):
        item = self.list.currentItem()
        if not item:
            QMessageBox.warning(self, "Select", "Select a task.")
            return
        # We stored the task id in Qt.UserRole
        task_id = item.data(32)  # Qt.UserRole
        assignee = item.data(33) # Qt.UserRole + 1
        if self._assign_dialog_opener:
            self._assign_dialog_opener(task_id, assignee)

    def show_tasks(self, mode="view_my_tasks", current_user=None, role=None, context=None):
        self._last_mode, self._last_user, self._last_role = mode, current_user, role
        if context:
            self._context = context
        base_id = self._context.get("base_id")
        tail = self._context.get("tail")

        all_tasks = filter_tasks(base_id=base_id, aircraft_tail=tail)
        self.list.clear()

        if mode == "view_all_tasks" and role == "admin":
            shown = all_tasks
            header = f"All Work Orders @ {base_id} / {tail}"
        elif mode == "repair_requests":
            shown = [t for t in all_tasks if "repair" in t.get("title", "").lower()]
            header = f"Repair Requests @ {base_id} / {tail}"
        else:
            shown = [t for t in all_tasks if t.get("assigned_to") == current_user]
            header = f"My Work Orders ({current_user}) @ {base_id} / {tail}"

        self.info.setText(header)

        for t in shown:
            tid   = t.get("id")
            title = t.get("title", "Untitled")
            status = t.get("status", "pending")
            assigned = t.get("assigned_to") or "Unassigned"
            line = f"#{tid}  •  {title}  •  {assigned}"

            item = QListWidgetItem(line)
            # colored dot as a "chip"
            item.setIcon(_dot(STATUS_COLORS.get(status, "#9aa4b2")))
            # store metadata for later
            item.setData(32, tid)         # task id
            item.setData(33, assigned if assigned != "Unassigned" else None)
            item.setToolTip(f"Status: {status.replace('_', ' ').title()}")
            self.list.addItem(item)

    def mark_selected_complete(self, current_user=None):
        if not self._perms.get("can_mark_complete", True):
            QMessageBox.warning(self, "Not Allowed", "You are not allowed to mark completion.")
            return

        if current_user is None:
            current_user = self._last_user

        row = self.list.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Select a task first.")
            return

        item = self.list.item(row)
        task_id = item.data(32)

        # Only allow completion if the task is in current context
        base_id = self._context.get("base_id")
        tail = self._context.get("tail")

        tasks = load_tasks()
        for t in tasks:
            if t.get("id") == task_id:
                if t.get("base_id") != base_id or t.get("aircraft_tail") != tail:
                    QMessageBox.warning(self, "Context", "Task is not in the selected base/aircraft.")
                    return
                if current_user and t.get("assigned_to") not in (current_user, None):
                    QMessageBox.warning(self, "Not Allowed", "You cannot complete someone else’s task.")
                    return
                t["status"] = "completed"
                save_tasks(tasks)
                self.show_tasks(self._last_mode, self._last_user, self._last_role, self._context)
                QMessageBox.information(self, "Done", f"Work Order #{task_id} marked completed.")
                return

        QMessageBox.warning(self, "Not Found", "Task not found.")
