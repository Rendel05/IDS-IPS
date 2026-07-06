from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

from ui.components.mini_badge import mini_badge


class DeviceRow(QWidget):

    def __init__(self, mac, info):
        super().__init__()

        self.setStyleSheet(
            'margin-right: 20px;'
        )
        layout = QHBoxLayout(self)

        layout.addWidget(QLabel(f'Dirección IP {info["ip"]}'))
        layout.addWidget(QLabel(f'Dirección MAC {mac.upper()}'))
        layout.addWidget(QLabel(f'Fabricante {info["vendor"]}'))

        layout.addWidget(
            mini_badge(
                "Gateway" if info["is_gateway"] else "Dispositivo",
                "alta" if info["is_gateway"] else "media"
            )
        )

        layout.addStretch()