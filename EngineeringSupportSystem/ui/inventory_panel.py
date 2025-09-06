# ui/inventory_panel.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QLineEdit, QPushButton, QMessageBox
from inventory_store import load_stock, save_stock, upsert_item, adjust_qty, delete_item, low_stock

class InventoryPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.list = QListWidget()
        self.low_label = QLabel("")
        self.part_no = QLineEdit(); self.part_no.setPlaceholderText("Part No.")
        self.name = QLineEdit(); self.name.setPlaceholderText("Part Name")
        self.qty = QLineEdit(); self.qty.setPlaceholderText("Qty")
        self.min_qty = QLineEdit(); self.min_qty.setPlaceholderText("Min Qty")

        add_btn = QPushButton("Add/Update")
        add_btn.clicked.connect(self._add_update)

        del_btn = QPushButton("Delete")
        del_btn.clicked.connect(self._delete)

        inc_btn = QPushButton("+ Qty")
        inc_btn.clicked.connect(lambda: self._adjust(1))
        dec_btn = QPushButton("- Qty")
        dec_btn.clicked.connect(lambda: self._adjust(-1))

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh)

        top = QHBoxLayout()
        top.addWidget(self.part_no); top.addWidget(self.name)
        top.addWidget(self.qty); top.addWidget(self.min_qty)
        top.addWidget(add_btn)

        bar = QHBoxLayout()
        bar.addWidget(del_btn); bar.addWidget(inc_btn); bar.addWidget(dec_btn); bar.addWidget(refresh_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Inventory"))
        layout.addWidget(self.list)
        layout.addLayout(top)
        layout.addLayout(bar)
        layout.addWidget(self.low_label)

        self.refresh()

    def refresh(self):
        self.list.clear()
        for it in load_stock():
            flag = "⚠️" if it.get("qty", 0) < it.get("min_qty", 0) else ""
            self.list.addItem(f"{it['part_no']} | {it['name']} | qty={it['qty']} | min={it['min_qty']} {flag}")
        lows = low_stock()
        self.low_label.setText(f"Low stock: {len(lows)} item(s)")

    def _add_update(self):
        try:
            upsert_item(
                self.part_no.text().strip(),
                self.name.text().strip(),
                int(self.qty.text() or 0),
                int(self.min_qty.text() or 0),
            )
            QMessageBox.information(self, "Saved", "Item saved.")
            self.refresh()
        except ValueError:
            QMessageBox.warning(self, "Error", "Qty and Min Qty must be numbers.")

    def _selected_part(self):
        item = self.list.currentItem()
        if not item: return None
        return item.text().split("|")[0].strip()

    def _delete(self):
        p = self._selected_part()
        if not p: QMessageBox.warning(self, "Select", "Select an item."); return
        if delete_item(p):
            QMessageBox.information(self, "Deleted", f"{p} removed.")
            self.refresh()
        else:
            QMessageBox.warning(self, "Error", "Could not delete.")

    def _adjust(self, d: int):
        p = self._selected_part()
        if not p: QMessageBox.warning(self, "Select", "Select an item."); return
        if adjust_qty(p, d):
            self.refresh()
        else:
            QMessageBox.warning(self, "Error", "Item not found.")
