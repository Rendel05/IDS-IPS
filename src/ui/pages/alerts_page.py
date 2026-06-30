from PySide6.QtCore import Qt, QSize, QSignalBlocker
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QComboBox, \
    QTableWidget, QHeaderView, QAbstractItemView, QSizePolicy

from services.database_manager import DatabaseManager
from ui.components.button import standard_button
from services.icons_manager import IconManager
from services.settings_manager import SettingsManager
from ui.delegates.dashboard_table_manager import TotalAlertsController
from ui.delegates.alert_details import AlertDetails



class AlertsPage(QWidget):
    PAGE_SIZE = 10

    def __init__(self):
        super().__init__()


        self.layout = QVBoxLayout()
        self.settings = SettingsManager()
        self.db = DatabaseManager()
        self.icon_manager = IconManager(self.settings)
        self.icon = IconManager(self.settings)



        title_layout = QVBoxLayout()
        title_label = QLabel("Alertas")
        title_label.setProperty('class', 'content_title')
        title_description = QLabel("Módulo de consulta de alertas generadas.")
        title_description.setProperty('class', 'content_subtitle')
        title_layout.addWidget(title_label)
        title_layout.addWidget(title_description)

        title = QWidget()
        title.setLayout(title_layout)
        title.setFixedHeight(70)

        self.filters_layout = QHBoxLayout()


        text_search_layout = QVBoxLayout()
        self.search_area = QLineEdit()
        self.search_area.setPlaceholderText("Buscar por firma o IP...")
        self.search_area.textChanged.connect(
            self.reset_filters_handler
        )

        text_search_layout.addWidget(self.search_area)

        text_search = QWidget()
        text_search.setLayout(text_search_layout)
        text_search.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)


        severity_options_layout = QVBoxLayout()
        self.severity_options = QComboBox()
        self.severity_options.addItem(" Todas",0)
        self.severity_options.addItem(" Baja", 1)
        self.severity_options.addItem(" Media", 2)
        self.severity_options.addItem(" Alta", 3)
        self.severity_options.addItem(" Crítica",4)
        self.severity_options.currentIndexChanged.connect(
            self.reset_filters_handler
        )

        severity_options_layout.addWidget(self.severity_options)

        severity_filter = QWidget()
        severity_filter.setLayout(severity_options_layout)


        date_filter_layout = QHBoxLayout()
        self.date_options = QComboBox()
        self.date_options.addItem(" Todas", 0)
        self.date_options.addItem(" Últimas 24 horas", 1)
        self.date_options.addItem(" Últimas 48 horas", 2)
        self.date_options.addItem(" Últimos 7 días", 3)
        self.date_options.currentIndexChanged.connect(
            self.reset_filters_handler
        )

        date_filter_layout.addWidget(self.date_options)

        date_filter = QWidget()
        date_filter.setLayout(date_filter_layout)



        self.search_button = standard_button("Aplicar filtros")
        self.search_button.setIcon(self.icon_manager.get("search"))
        self.search_button.clicked.connect(
            self.add_filters
        )
        self.delete_button = standard_button("Vaciar alertas")
        self.delete_button.setIcon(self.icon_manager.get("trash"))

        self.erase_filters = standard_button("Limpiar filtros")
        self.erase_filters.setIcon(self.icon_manager.get("eraser"))
        self.erase_filters.hide()
        self.erase_filters.clicked.connect(
            lambda : self.reset_filters()
        )

        self.filters_layout.addWidget(text_search)
        self.filters_layout.addWidget(severity_filter)
        self.filters_layout.addWidget(date_filter)
        self.filters_layout.addWidget(self.erase_filters)
        self.filters_layout.addWidget(self.search_button)
        self.filters_layout.addWidget(self.delete_button)


        filters = QWidget()
        filters.setLayout(self.filters_layout)
        filters.setProperty('class', 'content_card')
        filters.setContentsMargins(0,-10,0,-10)
        filters.setMaximumHeight(40)

        #layout principal de contenido
        self.alerts_main_layout = QHBoxLayout()

        alerts_container_layout = QVBoxLayout()
        title_container = QLabel('Lista de alertas')
        title_container.setProperty('class','card_title')
        self.alerts_table = QTableWidget()
        self.alerts_table.setColumnCount(4)
        self.alerts_table.setHorizontalHeaderLabels(
            ['Hora','Severidad','Firma','Origen']
        )
        self.alerts_table.setObjectName('recent_alerts_table')
        self.alerts_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.alerts_table.setShowGrid(False)
        self.alerts_table.verticalHeader().setVisible(False)
        self.alerts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_controller = TotalAlertsController(
            self.alerts_table, self.db
        )
        self.table_controller.refresh()
        self.alerts_table.cellClicked.connect(
            self.on_alert_selected
        )



        alerts_container_layout.addWidget(title_container)
        alerts_container_layout.addWidget(self.alerts_table)


        alerts_container = QWidget()
        alerts_container.setLayout(alerts_container_layout)
        alerts_container.setProperty('class','content_card')
        alerts_container.setFixedHeight(400)

        self.alerts_details_layout = QVBoxLayout()
        title_details = QLabel('Detalles de la alerta')
        title_details.setProperty('class','card_title')
        self.alerts_details_layout.addWidget(title_details)
        self.alerts_details_controller = AlertDetails(self.alerts_details_layout)



        self.alerts_details_layout.addStretch()
        self.alerts_details = QWidget()
        self.alerts_details.setLayout(self.alerts_details_layout)
        self.alerts_details.setProperty('class','content_card')
        self.alerts_details.setFixedSize(320, 400)
        self.alerts_details.hide()


        self.alerts_main_layout.addWidget(alerts_container)
        self.alerts_main_layout.addWidget(self.alerts_details)

        alerts_main = QWidget()
        alerts_main.setLayout(self.alerts_main_layout)

        self.paging_layout = QHBoxLayout()

        self.prev_page = standard_button('')
        self.next_page = standard_button('')
        self.prev_page.setIcon(self.icon.get('arrow-left-circle'))
        self.next_page.setIcon(self.icon.get('arrow-right-circle'))
        self.current_page = QLabel(f'Página {self.table_controller.current_page} de {self.table_controller.pages}')
        self.paging_layout.addWidget(self.prev_page)
        self.paging_layout.addWidget(self.current_page)
        self.paging_layout.addWidget(self.next_page)
        self.paging_layout.addStretch()

        self.prev_page.clicked.connect(
            lambda : self.change_page(0)
        )
        self.next_page.clicked.connect(
            lambda : self.change_page(1)
        )

        self.paging = QWidget()
        self.paging.setLayout(self.paging_layout)
        self.paging.setProperty('class','content_card')
        self.update_pagination_state()



        self.paging_layout = QHBoxLayout()
        self.layout.addWidget(title)
        self.layout.addWidget(filters)
        self.layout.addWidget(alerts_main)
        self.layout.addWidget(self.paging)
        self.layout.addStretch()


        self.setLayout(self.layout)

    def change_theme(self):

        self.settings = SettingsManager()
        self.icon_manager = IconManager(self.settings)
        self.erase_filters.setIcon(self.icon_manager.get('eraser'))
        self.search_button.setIcon(self.icon_manager.get('search'))
        self.delete_button.setIcon(self.icon_manager.get('trash'))
        self.prev_page.setIcon(self.icon_manager.get('arrow-left-circle'))
        self.next_page.setIcon(self.icon_manager.get('arrow-right-circle'))

    def get_current_filters(self):
        return {
            "limit": self.PAGE_SIZE,
            "search": self.search_area.text().strip(),
            "date_filter": self.date_options.currentData(),
            "severity_filter": self.severity_options.currentData()
        }

    def load_alerts_page(self, page):
        self.table_controller.records = self.db.get_alerts(
            page=page,
            **self.get_current_filters()
        )
        self.table_controller.refresh()
        self.update_pagination_state()

    def update_pagination_state(self):
        current_page = self.table_controller.current_page
        pages = self.table_controller.pages

        self.current_page.setText(f'Página {current_page} de {pages}')
        self.prev_page.setEnabled(current_page > 1)
        self.next_page.setEnabled(current_page < pages)

    def change_page(self,position):
        if position == 0:
            target_page = self.table_controller.current_page - 1
        elif position == 1:
            target_page = self.table_controller.current_page + 1
        else:
            return

        if target_page < 1 or target_page > self.table_controller.pages:
            self.update_pagination_state()
            return

        self.load_alerts_page(target_page)

    def on_alert_selected(self):
        row = self.alerts_table.currentRow()
        item = self.alerts_table.item(row, 0)
        if item is None:
            return

        alert_id = item.data(Qt.UserRole)
        self.alerts_details_controller.refresh(alert_id)
        self.alerts_details.show()

    def add_filters(self):
        self.load_alerts_page(1)

    def reset_filters_handler(self):
        if self.search_area.text().strip() != '' or self.severity_options.currentIndex() != 0 or self.date_options.currentIndex() != 0:
            self.erase_filters.show()
        else:
            self.erase_filters.hide()

    def reset_filters(self):
        with QSignalBlocker(self.search_area):
            self.search_area.setText('')

        with QSignalBlocker(self.severity_options):
            self.severity_options.setCurrentIndex(0)

        with QSignalBlocker(self.date_options):
            self.date_options.setCurrentIndex(0)

        self.load_alerts_page(1)
        self.reset_filters_handler()