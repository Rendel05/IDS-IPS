from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QComboBox, QHBoxLayout, QApplication
from PySide6.QtCore import Signal

from ui.components.button import standard_button

from services.settings_manager import SettingsManager
from ui.styles.loader import load_stylesheet
from ui.components.confirm_dialog import SweetAlert




class SettingsPage(QWidget):
    theme_changed = Signal()
    engine_paused = Signal(bool)

    def __init__(self, app: QApplication):
        super().__init__()

        self.app = app
        self.settings = SettingsManager()

        layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        title_label = QLabel("Configuración")
        title_label.setProperty('class', 'content_title')
        title_description = QLabel("Configuración de parámetros del motor y preferencias.")
        title_description.setProperty('class', 'content_subtitle')
        title_layout.addWidget(title_label)
        title_layout.addWidget(title_description)

        title = QWidget()
        title.setLayout(title_layout)
        title.setFixedHeight(70)

        filters_layout = QVBoxLayout()
        filters_title = QLabel("Filtros del motor")
        filters_title.setProperty('class', 'content_title')
        filters_description = QLabel('Selecciona que eventos captar o ignorar.')

        self.icmp = QCheckBox("Inundación ICMP")
        self.icmp.setChecked(self.settings.get('detectors', 'icmp_flood'))
        self.bind_checkbox(self.icmp, 'detectors', 'icmp_flood')
        self.icmp.setToolTip("Detectar un volumen anormalmente alto de tráfico ICMP (ping)")
        self.ip_change = QCheckBox("Reasignación de IP")
        self.ip_change.setChecked(self.settings.get('detectors', 'ip_changes'))
        self.bind_checkbox(self.ip_change, 'detectors', 'ip_changes')
        self.ip_change.setToolTip('Dectecar un cambio de la IP asignada por el DHCP')
        self.sniffer = QCheckBox("Sniffer detectado")
        self.sniffer.setChecked(self.settings.get('detectors', 'packet_sniffer'))
        self.bind_checkbox(self.sniffer, 'detectors', 'packet_sniffer')
        self.sniffer.setToolTip('Detectar un dispositivo en modo promiscuo')
        self.nmap = QCheckBox("Escaneo de puertos")
        self.nmap.setChecked(self.settings.get('detectors', 'nmap_scan'))
        self.bind_checkbox(self.nmap, 'detectors', 'nmap_scan')
        self.nmap.setToolTip("Detectar posibles escaneo de puertos y servicios abiertos")
        self.new_port = QCheckBox('Nuevo puerto abierto')
        self.new_port.setChecked(self.settings.get('detectors', 'new_port'))
        self.bind_checkbox(self.new_port, 'detectors', 'new_port')
        self.beaconing = QCheckBox('Señal periódica detectada')
        self.beaconing.setChecked(self.settings.get('detectors', 'beaconing'))
        self.bind_checkbox(self.beaconing, 'detectors', 'beaconing')
        self.beaconing.setToolTip("Detectar tráfico continúo inusual")
        self.device = QCheckBox('Dispositivo activado')
        self.device.setChecked(self.settings.get('detectors', 'new_device'))
        self.bind_checkbox(self.device, 'detectors', 'new_device')

        filters_layout.addWidget(filters_title)
        filters_layout.addWidget(filters_description)
        filters_layout.addWidget(self.icmp)
        filters_layout.addWidget(self.ip_change)
        filters_layout.addWidget(self.sniffer)
        filters_layout.addWidget(self.nmap)
        filters_layout.addWidget(self.new_port)
        filters_layout.addWidget(self.beaconing)
        filters_layout.addWidget(self.device)
        filters = QWidget()
        filters.setLayout(filters_layout)
        filters.setProperty('class', 'content_card')

        system_status_layout = QVBoxLayout()
        system_status_title = QLabel("Sistema y arranque")
        self.autostart = QCheckBox("Iniciar el programa automáticamente al arrancar el sistema")
        self.autostart.setChecked(self.settings.get('general', 'launch_on_startup'))
        self.bind_checkbox(self.autostart, 'general', 'launch_on_startup')
        self.pause_engine = standard_button("")
        if not self.settings.get('monitoring', 'on_paused'):
            self.pause_engine.setText('Pausar el motor')
        else:
            self.pause_engine.setText('Reanudar el motor')
        self.pause_engine.clicked.connect(
            self.pause_detection
        )

        system_status_title.setProperty('class', 'content_title')

        system_status_layout.addWidget(system_status_title)
        system_status_layout.addWidget(QLabel('Estado del sistema y configuración de arranque'))
        system_status_layout.addWidget(self.autostart)
        system_status_layout.addWidget(self.pause_engine)
        system_status = QWidget()
        system_status.setLayout(system_status_layout)
        system_status.setProperty('class', 'content_card')

        miscellaneous_layout = QVBoxLayout()

        miscellaneous_title = QLabel("Varios")
        miscellaneous_title.setProperty('class', 'content_title')
        theme_layout = QHBoxLayout()
        self.theme = QComboBox()
        self.theme.addItem(' Oscuro', 'dark')
        self.theme.addItem(' Claro', 'light')
        theme = self.settings.get('ui', 'theme')
        index = self.theme.findData(theme)
        if index >= 0:
            self.theme.setCurrentIndex(index)
        self.theme.currentIndexChanged.connect(self.save_theme)
        self.theme.currentIndexChanged.connect(self.change_theme)
        theme_layout.addWidget(QLabel('Cambiar apariencia del sistema'))
        theme_layout.addWidget(self.theme)
        theme_layout.addStretch()
        theme_widget = QWidget()
        theme_widget.setLayout(theme_layout)

        miscellaneous_layout.addWidget(miscellaneous_title)
        miscellaneous_layout.addWidget(QLabel('Configuración extra del sistema'))
        miscellaneous_layout.addWidget(theme_widget)
        self.notifications = QCheckBox('Permitir notificaciones')
        self.notifications.setChecked(self.settings.get('notifications', 'enabled'))
        self.bind_checkbox(self.notifications, 'notifications', 'enabled')
        miscellaneous_layout.addWidget(self.notifications)

        miscellaneous = QWidget()
        miscellaneous.setLayout(miscellaneous_layout)
        miscellaneous.setProperty('class', 'content_card')

        self.restart_layout = QHBoxLayout()
        self.restart_label = QLabel('Los cambios requieren reiniciar el sistema')
        self.restart_button = standard_button("Reiniciar ahora")
        self.restart_button.clicked.connect(
            lambda : print(
                'Ac[a va a ir la l[ogica del reinicio, no tengo idea de c[omo implementar eso a[un ¯\\_(ツ)_/¯')
        )
        self.restart_layout.addStretch()
        self.restart_layout.addWidget(self.restart_label)
        self.restart_layout.addWidget(self.restart_button)
        self.restart_widget = QWidget()
        self.restart_widget.setLayout(self.restart_layout)

        layout.addWidget(title)
        layout.addWidget(filters)
        layout.addWidget(system_status)
        layout.addWidget(miscellaneous)
        layout.addWidget(self.restart_widget)
        layout.addStretch()

        self.setLayout(layout)

    def bind_checkbox(self, checkbox, section, key):
        checkbox.setChecked(
            self.settings.get(section, key)
        )

        checkbox.toggled.connect(
            lambda checked:
            self.settings.set(
                checked,
                section,
                key
            )
        )

    def save_theme(self, *_):
        value = self.theme.currentData()

        self.settings.set(
            value,
            "ui",
            "theme"
        )

    def pause_detection(self):
        status = self.settings.get('monitoring', 'on_paused')
        if not status:
            confirmed = SweetAlert.confirm(
                parent=self,
                title="¿Seguro que quieres pausar el sistema?",
                text='Los detectores dejaran de percibir actividad'
            )
            if confirmed:
                self.pause_engine.setText("Reanudar el motor")
                self.settings.set(
                    not status,
                    "monitoring",
                    "on_paused"
                )
                self.engine_paused.emit(not status)
        else:
            self.pause_engine.setText("Pausar el motor")
            self.settings.set(
                not status,
                "monitoring",
                "on_paused"
            )
            self.engine_paused.emit(not status)

    def change_theme(self, *_):

        theme = self.theme.currentData()

        self.settings.set(
            theme,
            "ui",
            "theme"
        )

        if self.app is not None:
            self.app.setStyleSheet(load_stylesheet(theme))

        self.theme_changed.emit()
