import sys

from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

from services.global_updater import GlobalUpdater
from ui.main_page import MainWindow
from ui.styles.loader import load_stylesheet
from services.database_manager import DatabaseManager
from services.settings_manager import SettingsManager
from core.packet_capture import PacketCapture
from core.detection_engine import DetectionEngine
from services.alerts_manager import AlertManager

from core.detectors.icmp_flood import ICMPFloodDetector
from core.monitors.dhcp_change import IPMonitor
from core.monitors.new_port import PortMonitor
from core.detectors.beaconing import BeaconDetector
from core.monitors.new_device import DeviceMonitor
from core.detectors.port_scan import ScanDetector



class Application:

    def __init__(self, qt_app: QApplication):
        self.qt_app = qt_app

        # ----------------- Services -----------------

        self.db = DatabaseManager()
        self.settings = SettingsManager()

        self.settings.set(False, "monitoring", "on_paused")

        self.alert_service = AlertManager(self.db)

        self.updater = GlobalUpdater()

        # ----------------- Monitors  -----------------

        self.dhcp_monitor = IPMonitor(
            self.settings,
            self.alert_service.create_alert,
            self.updater
        )

        self.ports_monitor = PortMonitor(
            self.settings,
            self.alert_service.create_alert,
            self.updater
        )

        self.device_monitor = DeviceMonitor(
            self.settings,
            self.alert_service.create_alert,
            self.updater
        )

        self.monitors = [
            self.dhcp_monitor,
            self.ports_monitor,
            self.device_monitor
        ]

        # ----------------- Detectores -----------------

        self.icmp_detector = ICMPFloodDetector(
            self.settings,
            self.alert_service.create_alert,
            self.updater
        )

        self.beacon_detector = BeaconDetector(
            self.settings,
            self.alert_service.create_alert,
            self.updater
        )

        self.port_scan_detector = ScanDetector(
            self.settings,
            self.alert_service.create_alert,
            self.updater
        )

        self.detectors = [
            self.icmp_detector,
            self.beacon_detector,
            self.port_scan_detector
        ]

        self.detection_engine = DetectionEngine(
            detectors=self.detectors
        )

        self.packet_capture = PacketCapture(
            self.detection_engine.process
        )

        # ----------------- UI -----------------

        self.qt_app.setStyleSheet(
            load_stylesheet(
                self.settings.get("ui", "theme")
            )
        )

        self.window = MainWindow(
            self
        )

        self.setup_tray()

        self.qt_app.aboutToQuit.connect(
            self.cleanup
        )

    # ------------------------------------------------

    def setup_tray(self):

        self.tray = QSystemTrayIcon(
            QIcon("assets/node.png"),
            self.window
        )

        self.tray.activated.connect(
            self.handle_tray_activation
        )

        menu = QMenu()

        show_action = QAction(
            "Mostrar ventana",
            self.window
        )

        exit_action = QAction(
            "Salir",
            self.window
        )

        show_action.triggered.connect(
            self.window.show_from_tray
        )

        exit_action.triggered.connect(
            QApplication.quit
        )

        menu.addAction(show_action)
        menu.addSeparator()
        menu.addAction(exit_action)

        self.tray.setContextMenu(menu)
        self.tray.show()

    # ------------------------------------------------

    def handle_tray_activation(self, reason):

        if reason == QSystemTrayIcon.Trigger:
            self.window.show_from_tray()

    # ------------------------------------------------

    def start(self):

        self.window.show()

        self.packet_capture.start()

        for monitor in self.monitors:
            monitor.start()

    # ------------------------------------------------

    def stop(self):

        self.packet_capture.stop()

        for monitor in self.monitors:
            monitor.stop()

    # ------------------------------------------------

    def restart_monitoring(self):

        self.stop()

        # Aquí después podrás reconstruir detectores,
        # packet capture, engine, etc.

        self.start()

    # ------------------------------------------------

    def cleanup(self):

        self.stop()

        self.db.close()


def main():

    qt_app = QApplication(sys.argv)

    application = Application(qt_app)

    application.start()

    sys.exit(qt_app.exec())


if __name__ == "__main__":
    main()