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



def main():
    app = QApplication(sys.argv)

    #Instancia de la DB y del JSON de configuración
    db = DatabaseManager()
    settings = SettingsManager()

    settings.set(False,"monitoring","on_paused")

    alert_service = AlertManager(db)

    updater = GlobalUpdater()

    dhcp_monitor = IPMonitor(settings, alert_service.create_alert,updater)
    ports_monitor = PortMonitor(settings,alert_service.create_alert,updater)
    device_monitor = DeviceMonitor(settings, alert_service.create_alert,updater)
    device_monitor.start()


    icmp_detector = ICMPFloodDetector(settings, alert_service.create_alert,updater)
    beacon_detector = BeaconDetector(settings, alert_service.create_alert,updater)
    port_scan_detector = ScanDetector(settings, alert_service.create_alert,updater)


    detection_engine = DetectionEngine(
        detectors=[
            icmp_detector,
            beacon_detector,
            port_scan_detector
        ]
    )

    packet_capture = PacketCapture(
        detection_engine.process
    )

    app.setStyleSheet(
        load_stylesheet(settings.get('ui','theme'))
    )
    #--------------------MAIN WINDOW------------------------#
    window = MainWindow(app,device_monitor,updater)

    tray = QSystemTrayIcon(
        QIcon("assets/node.png"),
        window
    )

    def handle_tray_activation(reason):
        if reason == QSystemTrayIcon.Trigger:
            window.show_from_tray()

    tray.activated.connect(
        handle_tray_activation
    )

    tray_menu = QMenu()

    show_action = QAction(
        "Mostrar ventana",
        window
    )

    exit_action = QAction(
        "Salir",
        window
    )

    show_action.triggered.connect(
        window.show_from_tray
    )

    exit_action.triggered.connect(
        QApplication.quit
    )


    tray_menu.addAction(show_action)
    tray_menu.addSeparator()
    tray_menu.addAction(exit_action)

    tray.setContextMenu(tray_menu)

    tray.show()

    window.show()

    #Iniciar detectores y monitores
    packet_capture.start()
    dhcp_monitor.start()
    ports_monitor.start()


    def cleanup():
        packet_capture.stop()
        db.close()
        dhcp_monitor.stop()
        ports_monitor.stop()
        device_monitor.stop()

    app.aboutToQuit.connect(cleanup)

    sys.exit(app.exec())



if __name__ == "__main__":
    main()
