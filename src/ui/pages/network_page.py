from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from ui.pages.dashboard_page import set_path


class NetworkPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        title_layout = QVBoxLayout()
        title_label = QLabel("Red")
        title_label.setProperty('class', 'content_title')
        title_description = QLabel("Ventana de consulta de estado de red.")
        title_description.setProperty('class', 'content_subtitle')
        title_layout.addWidget(title_label)
        title_layout.addWidget(title_description)

        title = QWidget()
        title.setLayout(title_layout)
        title.setFixedHeight(70)

        gateway_layout = QVBoxLayout()

        gateway_container_layout = QHBoxLayout()
        gateway_icon= QLabel()
        pixmap= QPixmap('assets/gateway.svg')
        gateway_icon.setPixmap(pixmap)
        gateway_container_layout.addWidget(gateway_icon)
        gateway_container_layout.addWidget(QLabel("Dirección IP: 192.168.0.1"))
        gateway_container_layout.addWidget(QLabel('Dirección MAC: 00:00:07:AA:BB:CC'))
        gateway_container_layout.addWidget(QLabel('Dispositivo: Cisco'))
        gateway_container_layout.addStretch()

        gateway_container = QWidget()
        gateway_container.setStyleSheet("""
            margin-right: 20px;
        """)
        gateway_container.setLayout(gateway_container_layout)

        gateway_layout.addWidget(QLabel("Puerta de enlace predeterminada"))
        gateway_layout.addWidget(gateway_container)
        gateway= QWidget()
        gateway.setLayout(gateway_layout)
        gateway.setProperty('class', 'content_card')

        devices_layout = QVBoxLayout()

        rows_layout = QHBoxLayout()
        test1 = QLabel()
        pixmap2 = QPixmap('assets/unknow-device.svg')
        test1.setPixmap(pixmap2)
        rows_layout.addWidget(test1)
        rows_layout.addWidget(QLabel("Dirección IP: 192.168.0.2"))
        rows_layout.addWidget(QLabel('Dirección MAC: 00:00:07:AA:BB:CC'))
        rows_layout.addWidget(QLabel('Dispositivo: Lenovo'))
        rows_layout.addStretch()

        rows = QWidget()
        rows.setStyleSheet("""
                    margin-right: 20px;
                """)
        rows.setLayout(rows_layout)

        devices_layout.addWidget(QLabel("Dispositivos en la red"))
        devices_layout.addWidget(rows)
        devices = QWidget()
        devices.setLayout(devices_layout)
        devices.setProperty('class', 'content_card')

        layout.addWidget(title)
        layout.addWidget(gateway)
        layout.addWidget(devices)
        layout.addStretch()



        self.setLayout(layout)