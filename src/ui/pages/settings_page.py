from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QComboBox, QHBoxLayout, QToolTip

from ui.components.button import standard_button



class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
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
        filters_title= QLabel("Filtros del motor")
        filters_title.setProperty('class', 'content_title')
        filters_description = QLabel('Selecciona que eventos captar o ignorar.')

        icmp= QCheckBox("Inundación ICMP")
        icmp.setToolTip("Detectar un volumen anormalmente alto de tráfico ICMP (ping)")
        ip_change=QCheckBox("Reasignación de IP")
        ip_change.setToolTip('Dectecar un cambio de la IP asignada por el DHCP')
        sniffer = QCheckBox("Sniffer detectado")
        sniffer.setToolTip('Detectar un dispositivo en modo promiscuo')
        nmap = QCheckBox("Escaneo de puertos")
        nmap.setToolTip("Detectar posibles escaneo de puertos y servicios abiertos")
        new_port= QCheckBox('Nuevo puerto abierto')
        beaconing = QCheckBox('Señal periódica detectada')
        beaconing.setToolTip("Detectar tráfico continúo inusual")
        device = QCheckBox('Dispositivo activado')

        filters_layout.addWidget(filters_title)
        filters_layout.addWidget(filters_description)
        filters_layout.addWidget(icmp)
        filters_layout.addWidget(ip_change)
        filters_layout.addWidget(sniffer)
        filters_layout.addWidget(nmap)
        filters_layout.addWidget(new_port)
        filters_layout.addWidget(beaconing)
        filters_layout.addWidget(device)
        filters=QWidget()
        filters.setLayout(filters_layout)
        filters.setProperty('class', 'content_card')

        system_status_layout = QVBoxLayout()
        system_status_title = QLabel("Sistema y arranque")
        #pause_engine= QCheckBox("Pausar el sistema")
        autostart= QCheckBox("Iniciar el programa automáticamente")
        pause_engine = standard_button("Pausar el sistema")
        system_status_title.setProperty('class', 'content_title')

        system_status_layout.addWidget(system_status_title)
        system_status_layout.addWidget(QLabel('Estado del sistema y configuración de arranque'))
        system_status_layout.addWidget(autostart)
        system_status_layout.addWidget(pause_engine)
        system_status= QWidget()
        system_status.setLayout(system_status_layout)
        system_status.setProperty('class', 'content_card')


        miscellaneous_layout= QVBoxLayout()

        miscellaneous_title = QLabel("Varios")
        miscellaneous_title.setProperty('class', 'content_title')
        theme_layout= QHBoxLayout()
        theme = QComboBox()
        theme.addItem(' Oscuro')
        theme.addItem(' Claro')
        theme_layout.addWidget(QLabel('Cambiar apariencia del sistema'))
        theme_layout.addWidget(theme)
        theme_layout.addStretch()
        theme_widget = QWidget()
        theme_widget.setLayout(theme_layout)

        miscellaneous_layout.addWidget(miscellaneous_title)
        miscellaneous_layout.addWidget(QLabel('Configuración extra del sistema'))
        miscellaneous_layout.addWidget(theme_widget)

        miscellaneous=QWidget()
        miscellaneous.setLayout(miscellaneous_layout)
        miscellaneous.setProperty('class', 'content_card')


        layout.addWidget(title)
        layout.addWidget(filters)
        layout.addWidget(system_status)
        layout.addWidget(miscellaneous)
        layout.addStretch()

        self.setLayout(layout)