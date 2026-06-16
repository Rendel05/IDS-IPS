from PySide6 import QtGui
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QStackedWidget
from PySide6.QtCore import Qt

from ui.pages.devices_page import DevicesPage
from ui.pages.settings_page import SettingsPage
from ui.pages.alerts_page import AlertsPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.about_page import AboutPage
from ui.pages.network_page import NetworkPage

STATUS = 'Sistema activo'
STATUS_DESCRIPTION = 'Monitoreo en ejecución'
STATUS_ICON = 'online'


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Estilo básico general
        self.setWindowTitle("IDS/IPS")
        self.setWindowIcon(QtGui.QIcon('assets/node.png'))
        self.resize(1100, 730)
        self.setMinimumSize(1100, 730)
        self.setMaximumSize(1100, 730)

        main_layout = QHBoxLayout()
        sidebar_layout = QVBoxLayout()
        name_layout = QHBoxLayout()
        description_layout = QHBoxLayout()

        logo = QLabel()
        pixmap = QPixmap('assets/shield.png')
        pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)

        name = QLabel('IDS/IPS')
        name.setObjectName('name')

        name_layout.addWidget(logo)
        name_layout.addWidget(name)

        title = QWidget()
        title.setLayout(name_layout)
        title.setObjectName('title')

        description = QLabel('Sistema de detección de intrusiones')
        description.setObjectName('description')
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        description_layout.addWidget(description)

        subtitle = QWidget()
        subtitle.setLayout(description_layout)
        subtitle.setObjectName('subtitle')



        dashboard_btn = QPushButton(' Dashboard')
        dashboard_btn.setIcon(QtGui.QIcon('assets/home.svg'))
        dashboard_btn.setProperty('class', 'sidebar-button')

        alert_btn = QPushButton(' Alertas')
        alert_btn.setIcon(QtGui.QIcon('assets/alert.svg'))
        alert_btn.setProperty('class', 'sidebar-button')

        network_btn = QPushButton(' Red')
        network_btn.setIcon(QtGui.QIcon('assets/network.svg'))
        network_btn.setProperty('class', 'sidebar-button')

        devices_btn = QPushButton(" Periféricos")
        devices_btn.setIcon(QtGui.QIcon('assets/video-camera.svg'))
        devices_btn.setProperty('class', 'sidebar-button')

        settings_btn = QPushButton(' Configuración')
        settings_btn.setIcon(QtGui.QIcon('assets/settings.svg'))
        settings_btn.setProperty('class', 'sidebar-button')

        about_btn = QPushButton(' Acerca de')
        about_btn.setIcon(QtGui.QIcon('assets/information-circle.svg'))
        about_btn.setProperty('class', 'sidebar-button')

        status_layout = QHBoxLayout()
        icon_status_layout = QHBoxLayout()

        status_icon = QLabel('⏻')
        status_icon.setAlignment(Qt.AlignCenter)
        status_icon.setObjectName('status_icon')
        status_icon.setProperty("status", STATUS_ICON)

        icon_status_layout.addWidget(status_icon)

        icon_status = QWidget()
        icon_status.setFixedWidth(35)
        icon_status.setLayout(icon_status_layout)

        description_status_layout = QVBoxLayout()

        status_title = QLabel(STATUS)
        status_title.setWordWrap(True)
        status_title.setObjectName('status_title')

        description_status_layout.addWidget(status_title)

        status_description = QLabel(STATUS_DESCRIPTION)
        status_description.setObjectName('status_description')
        status_description.setWordWrap(True)

        description_status_layout.addWidget(status_description)

        description_status = QWidget()
        description_status.setLayout(description_status_layout)

        status_layout.addWidget(icon_status)
        status_layout.addWidget(description_status)

        status = QWidget()
        status.setLayout(status_layout)
        status.setObjectName('status')


        sidebar_layout.addWidget(title)
        sidebar_layout.addWidget(subtitle)
        sidebar_layout.addWidget(dashboard_btn)
        sidebar_layout.addWidget(alert_btn)
        sidebar_layout.addWidget(network_btn)
        sidebar_layout.addWidget(devices_btn)
        sidebar_layout.addWidget(settings_btn)
        sidebar_layout.addWidget(about_btn)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(status)

        sidebar = QWidget()
        sidebar.setLayout(sidebar_layout)
        sidebar.setFixedWidth(200)
        sidebar.setObjectName('sidebar')

        dashboard_page = DashboardPage()
        about_page = AboutPage()
        alerts_page = AlertsPage()
        network_page = NetworkPage()
        devices_page = DevicesPage()
        settings_page = SettingsPage()

        content = QStackedWidget()
        content.addWidget(dashboard_page)
        content.addWidget(about_page)
        content.addWidget(alerts_page)
        content.addWidget(network_page)
        content.addWidget(devices_page)
        content.addWidget(settings_page)
        content.setObjectName('content')

        dashboard_btn.clicked.connect(
            lambda :content.setCurrentWidget(dashboard_page)
        )

        about_btn.clicked.connect(
            lambda :content.setCurrentWidget(about_page)
        )

        alert_btn.clicked.connect(
            lambda :content.setCurrentWidget(alerts_page)
        )

        network_btn.clicked.connect(
            lambda :content.setCurrentWidget(network_page)
        )

        devices_btn.clicked.connect(
            lambda :content.setCurrentWidget(devices_page)
        )

        settings_btn.clicked.connect(
            lambda :content.setCurrentWidget(settings_page)
        )

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        self.setLayout(main_layout)
        self.setObjectName('main')

    def show_from_tray(self):
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def closeEvent(self, event):
        event.ignore()
        self.hide()