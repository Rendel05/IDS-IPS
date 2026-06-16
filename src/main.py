import sys

from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

from ui.main_page import MainWindow
from ui.styles.loader import load_stylesheet
from services.database_manager import DatabaseManager



def main():
    app = QApplication(sys.argv)
    #instancia de la DB
    db = DatabaseManager()

    app.setStyleSheet(
        load_stylesheet()
    )

    window = MainWindow()

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

    app.aboutToQuit.connect(
        db.close
    )

    sys.exit(app.exec())

if __name__ == "__main__":
    main()