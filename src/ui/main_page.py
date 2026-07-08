from PySide6 import QtGui
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QApplication
from PySide6.QtCore import Qt

from ui.pages.devices_page import DevicesPage
from ui.pages.settings_page import SettingsPage
from ui.pages.alerts_page import AlertsPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.about_page import AboutPage
from ui.pages.network_page import NetworkPage
from services.icons_manager import IconManager
from services.settings_manager import SettingsManager


#default_values
STATUS = 'Sistema activo'
STATUS_DESCRIPTION = 'Monitoreo en ejecución'
STATUS_ICON = 'online'


class MainWindow(QWidget):

    def __init__(self, app):
        super().__init__()
        # Estilo básico general
        self.setWindowTitle("IDS/IPS")
        self.setWindowIcon(QtGui.QIcon('assets/node.png'))
        self.resize(1100, 730)
        self.setMinimumSize(1100, 730)
        self.setMaximumSize(1100, 730)
        self.settings = SettingsManager()
        self.theme= '#FFFFFF' if self.settings.get('ui','theme') == 'light' else "#13171f"
        self.icon_manager = IconManager(self.settings)
        self.app = app



        main_layout = QHBoxLayout()
        sidebar_layout = QVBoxLayout()
        name_layout = QHBoxLayout()
        description_layout = QHBoxLayout()

        logo = QLabel()
        pixmap = QPixmap('assets/node.png')
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

        self.dashboard_btn = QPushButton(' Dashboard')
        self.dashboard_btn.setIcon(self.icon_manager.get('home'))
        self.dashboard_btn.setProperty('class', 'sidebar-button')

        self.alert_btn = QPushButton(' Alertas')
        self.alert_btn.setIcon(self.icon_manager.get('alert'))
        self.alert_btn.setProperty('class', 'sidebar-button')

        self.network_btn = QPushButton(' Red')
        self.network_btn.setIcon(self.icon_manager.get('network'))
        self.network_btn.setProperty('class', 'sidebar-button')

        self.devices_btn = QPushButton(" Periféricos")
        self.devices_btn.setIcon(self.icon_manager.get('video-camera'))
        self.devices_btn.setProperty('class', 'sidebar-button')

        self.settings_btn = QPushButton(' Configuración')
        self.settings_btn.setIcon(self.icon_manager.get('settings'))
        self.settings_btn.setProperty('class', 'sidebar-button')

        self.about_btn = QPushButton(' Acerca de')
        self.about_btn.setIcon(self.icon_manager.get('question-mark'))
        self.about_btn.setProperty('class', 'sidebar-button')

        status_layout = QHBoxLayout()

        icon_status_layout = QHBoxLayout()

        self.status_icon = QLabel('⏻')
        self.status_icon.setAlignment(Qt.AlignCenter)
        self.status_icon.setObjectName('status_icon')
        self.status_icon.setProperty("status", STATUS_ICON)

        icon_status_layout.addWidget(self.status_icon)

        icon_status = QWidget()
        icon_status.setFixedWidth(35)
        icon_status.setLayout(icon_status_layout)
        icon_status.setContentsMargins(-10, 0, 0, 0)

        description_status_layout = QVBoxLayout()

        self.status_title = QLabel(STATUS)
        self.status_title.setWordWrap(True)
        self.status_title.setObjectName('status_title')

        description_status_layout.addWidget(self.status_title)

        self.status_description = QLabel(STATUS_DESCRIPTION)
        self.status_description.setObjectName('status_description')
        self.status_description.setWordWrap(True)

        description_status_layout.addWidget(self.status_description)

        description_status = QWidget()
        description_status.setLayout(description_status_layout)
        description_status.setContentsMargins(-10, 0, 0, 0)

        status_layout.addWidget(icon_status)
        status_layout.addWidget(description_status)

        status = QWidget()
        status.setLayout(status_layout)
        status.setObjectName('status')


        sidebar_layout.addWidget(title)
        sidebar_layout.addWidget(subtitle)
        sidebar_layout.addWidget(self.dashboard_btn)
        sidebar_layout.addWidget(self.alert_btn)
        sidebar_layout.addWidget(self.network_btn)
        sidebar_layout.addWidget(self.devices_btn)
        sidebar_layout.addWidget(self.settings_btn)
        sidebar_layout.addWidget(self.about_btn)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(status)

        sidebar = QWidget()
        sidebar.setLayout(sidebar_layout)
        sidebar.setFixedWidth(200)
        sidebar.setObjectName('sidebar')

        self.dashboard_page = DashboardPage(self.theme)
        self.about_page = AboutPage()
        self.alerts_page = AlertsPage()
        self.alerts_page.clean.connect(
            lambda : self.dashboard_page.refresh_data()
        )
        self.network_page = NetworkPage()
        self.devices_page = DevicesPage(self.app.device_monitor)
        self.app.updater.device_signal.connect(
            self.devices_page.refresh
        )
        self.settings_page = SettingsPage(self.app)
        self.settings_page.theme_changed.connect(
            self.refresh_icons
        )
        self.settings_page.engine_paused.connect(
            self.engine_status
        )

        self.content = QStackedWidget()
        self.content.addWidget(self.dashboard_page)
        self.content.addWidget(self.about_page)
        self.content.addWidget(self.alerts_page)
        self.content.addWidget(self.network_page)
        self.content.addWidget(self.devices_page)
        self.content.addWidget(self.settings_page)
        self. content.setObjectName('content')


        self.dashboard_btn.clicked.connect(
            lambda :self.content.setCurrentWidget(self.dashboard_page)
        )

        self.about_btn.clicked.connect(
            lambda :self.content.setCurrentWidget(self.about_page)
        )

        self.alert_btn.clicked.connect(
            lambda :self.content.setCurrentWidget(self.alerts_page)
        )

        self.network_btn.clicked.connect(
            lambda :self.content.setCurrentWidget(self.network_page)
        )

        self.devices_btn.clicked.connect(
            lambda :self.content.setCurrentWidget(self.devices_page)
        )

        self.settings_btn.clicked.connect(
            lambda :self.content.setCurrentWidget(self.settings_page)
        )

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content)

        self.setLayout(main_layout)
        self.setObjectName('main')


        for page in (self.dashboard_page, self.alerts_page):
            self.app.updater.port_signal.connect(page.refresh_data)
            self.app.updater.icmp_signal.connect(page.refresh_data)
            self.app.updater.ip_signal.connect(page.refresh_data)
            self.app.updater.scan_signal.connect(page.refresh_data)
            self.app.updater.beacon_signal.connect(page.refresh_data)
            self.app.updater.device_signal.connect(page.refresh_data)


        #-------------------

    def show_from_tray(self):
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def closeEvent(self, event):
        event.ignore()
        self.hide()


    def refresh_icons(self):
        self.settings = SettingsManager()
        self.icon_manager = IconManager(self.settings)
        self.theme= '#FFFFFF' if self.settings.get('ui','theme') == 'light' else "#13171f"

        self.dashboard_page.change_theme(self.theme)
        self.about_page.change_theme()
        self.alerts_page.change_theme()
        self.network_page.change_theme()

        self.dashboard_btn.setIcon(self.icon_manager.get('home'))
        self.alert_btn.setIcon(self.icon_manager.get('alert'))
        self.network_btn.setIcon(self.icon_manager.get('network'))
        self.devices_btn.setIcon(self.icon_manager.get('video-camera'))
        self.settings_btn.setIcon(self.icon_manager.get('settings'))
        self.about_btn.setIcon(self.icon_manager.get('question-mark'))

    def engine_status(self,value):
        #values
        title = 'Sistema en pausa' if value else 'Sistema activo'
        description = 'Monitoreo suspendido' if value else 'Monitoreo en ejecución'
        icon = 'offline' if value else 'online'

        self.status_title.setText(title)
        self.status_description.setText(description)
        self.status_icon.setProperty('status', icon)
        self.status_icon.style().unpolish(self.status_icon)
        self.status_icon.style().polish(self.status_icon)
        self.status_icon.update()

