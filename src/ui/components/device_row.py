from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

from ui.components.mini_badge import mini_badge
from services.date_normalizer import normalize_datetime


def device_row(mac, info) -> QWidget:
    widget = QWidget()
    widget.setStyleSheet(
        "margin-right: 20px;"
    )

    layout = QHBoxLayout(widget)

    layout.addWidget(
        mini_badge(
            "Gateway" if info["is_gateway"] else "Dispositivo",
            "alta" if info["is_gateway"] else "media",
        )
    )

    layout.addWidget(QLabel(f'Dirección IP {info["ip"]}'))
    layout.addWidget(QLabel(f'Dirección MAC {mac.upper()}'))
    layout.addWidget(QLabel(f'Fabricante {info["vendor"]}'))
    layout.addWidget(
        QLabel(f'Última vez visto {normalize_datetime(info["last_seen"])}')
    )

    layout.addStretch()

    return widget