# ui/dashboards.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QMessageBox, QToolBar, QAction,
    QHBoxLayout, QPushButton, QScrollArea, QSizePolicy
)
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt

# App modules
from roles import ROLE_ACTIONS, ROLE_PERMS
from ui.labels import ROLE_DISPLAY, ACTION_LABELS
from ui.widgets.task_list_panel import TaskListPanel
from ui.task_editor import TaskEditorDialog
from ui.manage_users import ManageUsersDialog
from ui.approval_panel import ApprovalPanel
from ui.inventory_panel import InventoryPanel
from ui.training_panel import TrainingPanel
from ui.assign_task import AssignTaskDialog
from ui.summary_cards import SummaryCards
from ui.theme import icon_path, ASSETS
from base_store import load_bases, aircraft_by_base, base_name

# Map actions to toolbar icon filenames (created by generate_assets.py)
ICON_MAP = {
    "view_all_tasks": "tasks.png",
    "view_my_tasks": "tasks.png",
    "repair_requests": "tasks.png",
    "manage_users": "users.png",
    "approve_reject": "approve.png",
    "approve_reject_completed": "approve.png",
    "qc_approve": "approve.png",
    "create_task": "plus.png",
    "assign_task": "assign.png",
    "stock_levels": "inventory.png",
    "reorder_parts": "inventory.png",
    "training_schedule": "training.png",
    "cert_tracking": "training.png",
    "team_reports": "report.png",
    # utilities (no change-context icon since selector is inline)
    "logout": "logout.png",
}

# ---------- Inline Airbase → Aircraft selector ----------
class BaseAircraftSelector(QWidget):
    """
    Top section with:
      - row of Airbase buttons
      - row of Aircraft buttons (appears after a base is clicked)
    Calls on_select(base_id, tail) when an aircraft is chosen.
    """
    def __init__(self, on_select):
        super().__init__()
        self.on_select = on_select
        self._current_base = None

        self.main = QVBoxLayout(self)
        self.main.setContentsMargins(0, 0, 0, 8)
        self.main.setSpacing(6)

        # Airbases row (scrollable)
        self.base_row = self._make_scroll_row()
        self.main.addWidget(QLabel("Select Airbase"))
        self.main.addWidget(self.base_row["area"])

        # Aircraft row (scrollable)
        self.ac_row = self._make_scroll_row()
        self.ac_container = QWidget()
        ac_layout = QVBoxLayout(self.ac_container)
        ac_layout.setContentsMargins(0, 0, 0, 0)
        ac_layout.setSpacing(4)
        ac_layout.addWidget(QLabel("Select Aircraft (Tail)"))
        ac_layout.addWidget(self.ac_row["area"])
        self.ac_container.setVisible(False)
        self.main.addWidget(self.ac_container)

        self._populate_bases()

    def _make_scroll_row(self):
        holder = QWidget()
        h = QHBoxLayout(holder)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(8)
        h.addStretch(1)

        area = QScrollArea()
        area.setWidgetResizable(True)
        wrap = QWidget()
        wrap.setLayout(h)
        area.setWidget(wrap)
        return {"holder": holder, "layout": h, "wrap": wrap, "area": area}

    def _clear_row(self, row):
        layout = row["layout"]
        while layout.count() > 1:  # keep the final stretch
            item = layout.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)

    def _pill_button(self, text, style="#1f6feb"):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {style};
                color: white;
                border: 0;
                border-radius: 16px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{ filter: brightness(1.1); }}
            QPushButton:pressed {{ filter: brightness(0.9); }}
        """)
        btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        return btn

    def _populate_bases(self):
        self._clear_row(self.base_row)
        for b in load_bases():
            text = f"{base_name(b['id'])}"
            btn = self._pill_button(text)
            btn.clicked.connect(lambda _, bid=b["id"]: self._on_base(bid))
            self.base_row["layout"].insertWidget(self.base_row["layout"].count()-1, btn)

    def _on_base(self, base_id: str):
        self._current_base = base_id
        # Show aircraft row for this base
        self._clear_row(self.ac_row)
        ac_list = aircraft_by_base(base_id)
        if not ac_list:
            self.ac_container.setVisible(False)
            return
        for a in ac_list:
            text = f"{a['tail']}  •  {a['model']}"
            btn = self._pill_button(text, style="#0ea5e9")
            btn.clicked.connect(lambda _, tail=a["tail"]: self._on_aircraft(tail))
            self.ac_row["layout"].insertWidget(self.ac_row["layout"].count()-1, btn)
        self.ac_container.setVisible(True)

    def _on_aircraft(self, tail: str):
        if callable(self.on_select) and self._current_base:
            self.on_select(self._current_base, tail)


class DashboardWindow(QMainWindow):
    def __init__(self, username: str, role: str, context: dict):
        super().__init__()
        self.username = username
        self.role = role.lower()
        self.context = context or {"base_id": None, "tail": None}
        self.pretty_role = ROLE_DISPLAY.get(self.role, role.title())
        self._perms = ROLE_PERMS.get(self.role, {})

        # --- Window basics
        self.resize(1200, 760)
        self._init_bg()  # role wallpaper
        self.setWindowTitle(
            f"{self.pretty_role} - {self.username}   |   "
            f"{self.context.get('base_id') or 'No Base'} / {self.context.get('tail') or 'No Aircraft'}"
        )

        # --- Toolbar
        self.toolbar = QToolBar("Actions", self)
        self.addToolBar(self.toolbar)
        self._build_toolbar()

        # --- Central layout (title + chip + cards + selector + body)
        central = QWidget()
        self.setCentralWidget(central)
        self._layout = QVBoxLayout(central)

        title = QLabel(f"{self.pretty_role} {self.username}")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        chip_text = f"{self.context.get('base_id') or '—'} • {self.context.get('tail') or '—'}"
        context_chip = QLabel(chip_text)
        context_chip.setObjectName("contextChip")
        context_chip.setAlignment(Qt.AlignCenter)
        context_chip.setFixedHeight(28)
        self._context_chip = context_chip

        self._layout.addWidget(title)
        self._layout.addWidget(context_chip)

        # --- Summary cards
        self.cards = SummaryCards(self.context, self.username, self.role)
        self._layout.addWidget(self.cards)

        # --- Inline Base/Aircraft selector
        self.selector = BaseAircraftSelector(self._handle_inline_selection)
        self._layout.addWidget(self.selector)

        # --- Task panel
        self.panel = TaskListPanel()
        self.panel.set_context(self.context)
        self.panel.set_permissions({
            "can_assign": bool(self._perms.get("can_assign")),
            "can_mark_complete": bool(self._perms.get("can_mark_complete", True)),
        })
        self.panel.set_assign_dialog_opener(self._open_assign_dialog)
        self._layout.addWidget(self.panel)

    # -------------------------
    # Background wallpaper (role-based)
    # -------------------------
    def _init_bg(self):
        wp_role = ASSETS / "wallpapers" / f"{self.role}.jpg"
        wp_default = ASSETS / "aircraft.jpg"
        path = wp_role if wp_role.exists() else wp_default
        self._bg_pix = QPixmap(str(path)) if path.exists() else None
        self._apply_bg()

    def _apply_bg(self):
        if getattr(self, "_bg_pix", None):
            scaled = self._bg_pix.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            pal = self.palette()
            pal.setBrush(self.backgroundRole(), QBrush(scaled))
            self.setPalette(pal)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._apply_bg()

    # -------------------------
    # Toolbar
    # -------------------------
    def _build_toolbar(self):
        actions = ROLE_ACTIONS.get(self.role, [])
        for key, default_label in actions:
            pretty = ACTION_LABELS.get(key, default_label)
            icon_file = ICON_MAP.get(key)
            act = QAction(QIcon(icon_path(icon_file)) if icon_file else QIcon(), pretty, self)
            act.triggered.connect(lambda _, k=key: self.handle_action(k))
            self.toolbar.addAction(act)

    # -------------------------
    # Inline selector callback
    # -------------------------
    def _handle_inline_selection(self, base_id: str, tail: str):
        # Update context + header chip + refresh
        self.context = {"base_id": base_id, "tail": tail}
        self.setWindowTitle(f"{self.pretty_role} - {self.username}   |   {base_id} / {tail}")
        if hasattr(self, "_context_chip"):
            self._context_chip.setText(f"{base_id} • {tail}")

        # refresh cards + task panel
        self.cards.context = self.context
        self.cards.refresh()
        self.panel.set_context(self.context)
        self.panel.show_tasks(self.panel._last_mode, self.panel._last_user, self.panel._last_role, self.context)

    # -------------------------
    # Assign dialog bridge (called by TaskListPanel)
    # -------------------------
    def _open_assign_dialog(self, task_id: int, current_assignee: str | None):
        if not self._perms.get("can_assign"):
            QMessageBox.warning(self, "Not Allowed", "You cannot assign work orders.")
            return
        dlg = AssignTaskDialog(task_id=task_id, current_assignee=current_assignee, parent=self)
        if dlg.exec_():
            self.panel.show_tasks(self.panel._last_mode, self.panel._last_user, self.panel._last_role, self.context)

    # -------------------------
    # Action handler
    # -------------------------
    def handle_action(self, action_key: str):
        # Task views
        if action_key in ("view_my_tasks", "repair_requests", "view_all_tasks"):
            self.panel.show_tasks(mode=action_key, current_user=self.username, role=self.role, context=self.context)
            return

        # Create Work Order
        if action_key == "create_task":
            if not self._perms.get("can_create_task"):
                QMessageBox.warning(self, "Not Allowed", "You cannot create work orders.")
                return
            dlg = TaskEditorDialog(self, context=self.context)
            if dlg.exec_():
                self.panel.show_tasks(self.panel._last_mode, self.panel._last_user, self.panel._last_role, self.context)
            return

        # Assign
        if action_key == "assign_task":
            if not self._perms.get("can_assign"):
                QMessageBox.warning(self, "Not Allowed", "You cannot assign work orders.")
                return
            mode = "view_all_tasks" if self.role in ("admin", "manager", "planner", "scheduler", "flightops", "helpdesk") else "view_my_tasks"
            self.panel.show_tasks(mode=mode, current_user=self.username, role=self.role, context=self.context)
            return

        # Manage Users
        if action_key == "manage_users":
            if not self._perms.get("can_manage_users"):
                QMessageBox.warning(self, "Not Allowed", "You cannot manage users.")
                return
            ManageUsersDialog(self).exec_()
            return

        # Approvals
        if action_key in ("approve_reject", "approve_reject_completed", "qc_approve"):
            self._swap_body(ApprovalPanel())
            return

        # Inventory
        if action_key in ("stock_levels", "reorder_parts"):
            self._swap_body(InventoryPanel())
            return

        # Training
        if action_key in ("training_schedule", "cert_tracking"):
            self._swap_body(TrainingPanel(current_user=self.username, role=self.role))
            return

        QMessageBox.information(self, "Action", f"Action '{action_key}' clicked.")

    # -------------------------
    # Body swap helper (used for Approval/Inventory/Training panels)
    # -------------------------
    def _swap_body(self, widget: QWidget):
        # Remove current body (the last widget in layout)
        if self._layout.count() > 4:  # title, chip, cards, selector, body
            old = self._layout.itemAt(self._layout.count() - 1).widget()
            if old is not None:
                old.setParent(None)
        self._layout.addWidget(widget)
