from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout

from ui.components.device_row import device_row


class DeviceCard(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

    def refresh(self, devices: dict):
        self.clear()

        if not devices:
            self.layout.addWidget(QLabel("No se detectaron dispositivos"))
            return

        for mac, info in devices.items():
            self.layout.addWidget(device_row(mac, info))

    def clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()
