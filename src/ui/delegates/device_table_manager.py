from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem

TEXT_MAP = {
    "No access": "Sin acceso",
    "Blocked": "Bloqueado",
    "Access granted": "Acceso permitido",
    "ACTIVE (in use)": "ACTIVO (en uso)",
    "Inactive": "Inactivo",
    "No usage record": "Sin registros",
    "In use": "En uso",
}

class DeviceMonitor:
    def __init__(self, table, device_monitor):
        self.table = table
        self.device_monitor = device_monitor


    def refresh(self):
        snapshot = self.device_monitor.get_snapshot()

        self.table.clearContents()
        self.table.setRowCount(len(snapshot))

        for row, (app_name, info) in enumerate(snapshot.items()):

            values = (
                app_name,
                info["cam_access"],
                info["cam_state"],
                info["cam_last_used"],
                info["mic_access"],
                info["mic_state"],
                info["mic_last_used"],
            )

            for column, value in enumerate(values):
                display = TEXT_MAP.get(value, value)

                item = QTableWidgetItem(display)
                item.setToolTip(display)
                self.table.setItem(row, column, item)

        for row in range(self.table.rowCount()):
            for col in range(1, self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)

        self.table.resizeColumnsToContents()
