from time import sleep

from PySide6.QtCore import QTimer
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableView, QPushButton

from services.icons_manager import IconManager
from services.settings_manager import SettingsManager
from ui.components.button import standard_button
from ui.components.device_card import DeviceCard
from core.monitors.network_scanner import NetworkScanner



class NetworkPage(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()
        self.network = NetworkScanner()
        self.icon = IconManager(self.settings)
        self.refreshing = False

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


        devices_layout = QVBoxLayout()

        self.devices = DeviceCard()
        self.devices.refresh(self.network.scan())

        device_title = QLabel("Dispositivos en la red")
        device_title.setProperty('class', 'card_title')
        devices_layout.addWidget(device_title)
        devices_layout.addWidget(self.devices)
        devices = QWidget()
        devices.setLayout(devices_layout)
        devices.setProperty('class', 'content_card')

        refresh_layout = QHBoxLayout()
        self.refresh_label = QLabel("Escanear de nuevo")
        self.refresh_button = standard_button("")
        self.refresh_button.setIcon(self.icon.get('arrow-path'))
        self.refresh_button.clicked.connect(self.refresh)
        refresh_layout.addStretch()
        refresh_layout.addWidget(self.refresh_label)
        refresh_layout.addWidget(self.refresh_button)
        refresh_widget = QWidget()
        refresh_widget.setLayout(refresh_layout)

        layout.addWidget(title)
        layout.addWidget(devices)
        layout.addWidget(refresh_widget)
        layout.addStretch()



        self.setLayout(layout)

    def refresh(self):
        if self.refreshing:
            return

        self.refreshing = True

        self.refresh_button.setCursor(Qt.ForbiddenCursor)
        self.refresh_button.setProperty("busy", True)
        self.refresh_button.setToolTip(
            "Espera unos segundos antes de volver a actualizar."
        )

        self.devices.refresh(self.network.scan())

        QTimer.singleShot(5000, self.enable_refresh)

    def enable_refresh(self):
        self.refreshing = False
        self.refresh_button.setCursor(Qt.PointingHandCursor)
        self.refresh_button.setProperty("busy", False)
        self.refresh_button.setToolTip('')


    def change_theme(self):
        self.settings = SettingsManager()
        self.icon = IconManager(self.settings)
        self.refresh_button.setIcon(self.icon.get('arrow-path'))