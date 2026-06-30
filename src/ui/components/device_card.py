from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget
from services.pixmaps_manager import PixMapManager


class DeviceCard(QWidget):
    def __init__(self,device_type,ip,mac,device,settings):
        super().__init__()
        self.settings = settings
        self.icon_manager = PixMapManager(self.settings)
        self.device_type = device_type
        self.ip = ip
        self.mac = mac
        self.device = device

        self.layout = QHBoxLayout(self)

        self.icon = QLabel()
        self.ip_label = QLabel()
        self.mac_label = QLabel()
        self.device_label = QLabel()

        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.ip_label)
        self.layout.addWidget(self.mac_label)
        self.layout.addWidget(self.device_label)
        self.layout.addStretch()

        self.setStyleSheet("""
                            margin-right: 20px;
                        """)
        self.set()


    def set(self):

        self.icon.setPixmap(self.icon_manager.get(self.device_type))
        self.ip_label.setText(f'Dirección IP: {self.ip}')
        self.mac_label.setText(f'Dirección MAC: {self.mac}')
        self.device_label.setText(f'Dispositivo: {self.device}')
