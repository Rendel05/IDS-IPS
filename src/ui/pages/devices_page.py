from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QAbstractItemView, QHeaderView, \
    QSizePolicy, QHBoxLayout

from ui.delegates.device_table_manager import DeviceMonitor
from ui.delegates.physic_devices import PhysicCard


class DevicesPage(QWidget):
    def __init__(self,device_monitor):
        super().__init__()

        layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        title_label = QLabel("Dispositivos")
        title_label.setProperty('class', 'content_title')
        title_description = QLabel("Gestión y consulta de dispositivos periféricos del equipo.")
        title_description.setProperty('class', 'content_subtitle')
        title_layout.addWidget(title_label)
        title_layout.addWidget(title_description)
        self.device_monitor = device_monitor
        self.device_monitor.start()

        title = QWidget()
        title.setLayout(title_layout)
        title.setFixedHeight(70)

        self.physics_devices_layout = QHBoxLayout()

        self.cameras_devices_layout = QVBoxLayout()
        self.cameras_devices_title = QLabel('Cámaras detectadas')
        self.cameras_devices_title.setProperty('class', 'card_title')
        self.cameras_devices_layout.addWidget(self.cameras_devices_title)
        self.device_list = PhysicCard('cam',self.device_monitor, self.cameras_devices_layout)
        self.cameras_devices = QWidget()
        self.cameras_devices.setLayout(self.cameras_devices_layout)
        self.cameras_devices.setProperty('class', 'content_card')
        self.cameras_devices_layout.addStretch()

        self.microphones_devices_layout = QVBoxLayout()
        self.microphones_devices_title = QLabel('Micrófonos detectados')
        self.microphones_devices_title.setProperty('class', 'card_title')
        self.microphones_devices_layout.addWidget(self.microphones_devices_title)
        self.device_list = PhysicCard('mic',self.device_monitor, self.microphones_devices_layout)

        self.microphones_devices = QWidget()
        self.microphones_devices.setLayout(self.microphones_devices_layout)
        self.microphones_devices.setProperty('class', 'content_card')


        self.physics_devices_layout.addWidget(self.cameras_devices)
        self.physics_devices_layout.addWidget(self.microphones_devices)
        self.physics_devices = QWidget()
        self.physics_devices.setLayout(self.physics_devices_layout)
        self.physics_devices.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)



        # layout principal de contenido
        self.main_table_layout = QVBoxLayout()

        title_container = QLabel('Lista de aplicaciones con acceso')
        title_container.setProperty('class', 'card_title')
        self.device_table = QTableWidget()
        self.device_table.setColumnCount(7)
        self.device_table.setHorizontalHeaderLabels(
            ['App', 'Acceso a cámara', 'Estado', 'Última vez usado','Acceso a micrófono', 'Estado', 'Última vez usado']
        )

        self.device_table.setObjectName('device_table')
        self.device_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.device_table.setShowGrid(False)
        self.device_table.verticalHeader().setVisible(False)
        self.device_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.device_table.horizontalHeader().setStretchLastSection(False)
        self.device_table.horizontalHeader().setMinimumSectionSize(80)
        self.device_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.device_table.setObjectName('recent_alerts_table')

        self.table_manager = DeviceMonitor(self.device_table, self.device_monitor)
        self.table_manager.refresh()


        self.main_table_layout.addWidget(title_container)
        self.main_table_layout.addWidget(self.device_table)

        main_table = QWidget()
        main_table.setLayout(self.main_table_layout)
        main_table.setProperty('class', 'content_card')
        main_table.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)




        layout.addWidget(title)
        layout.addWidget(self.physics_devices)
        layout.addWidget(main_table)

        self.setLayout(layout)

    def refresh(self):
        self.table_manager.refresh()
        return


