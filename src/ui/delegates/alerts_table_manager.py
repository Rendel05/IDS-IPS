from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem

from ui.components.mini_badge import mini_badge


class RecentAlertsController:

    def __init__(self, table, db):
        self.table = table
        self.db = db

    def refresh(self):
        records = self.db.get_daily_alerts(5)

        self.table.clearContents()
        self.table.setRowCount(len(records))
        for row, record in enumerate(records):
            _, timestamp, severity, rule, source = record

            valid_rules = ("ICMP Flood","Sniffer","Port Scan",'Beaconing')
            real_source = source.split()[-1] if rule in valid_rules else "---"

            self.table.setItem(
                row, 0,
                QTableWidgetItem(timestamp[11:19])
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
