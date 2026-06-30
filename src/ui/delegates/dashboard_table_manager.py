from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem

from ui.components.mini_badge import mini_badge


class TotalAlertsController:

    def __init__(self, table, db):
        self.table = table
        self.db = db
        self.records = self.db.get_alerts(page=1)
        self.current_page = self.records["page"]
        self.pages = self.records["pages"]

    def refresh(self):
        self.current_page = self.records["page"]
        self.pages = self.records["pages"]

        self.table.clearContents()
        self.table.setRowCount(len(self.records["data"]))

        for row, record in enumerate(self.records["data"]):
            alert_id, timestamp, severity, rule, source = record

            valid_rules = ("ICMP Flood", "Sniffer", "Nmap Scan", "Beaconing")
            real_source = source.split()[-1] if rule in valid_rules else "---"

            time_item = QTableWidgetItem(timestamp[11:19])
            time_item.setData(Qt.UserRole, alert_id)

            self.table.setItem(
                row, 0,
                time_item
            )

            self.table.setCellWidget(
                row, 1,
                mini_badge(severity, severity)
            )

            self.table.setItem(
                row, 2,
                QTableWidgetItem(rule)
            )

            self.table.setItem(
                row, 3,
                QTableWidgetItem(real_source)
            )

        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)







