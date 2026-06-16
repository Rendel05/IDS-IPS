from PySide6 import QtGui
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QComboBox, QPushButton, \
    QTableWidget, QHeaderView
from ui.components import button
from ui.components.button import standard_button


class AlertsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

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

        filters_layout = QHBoxLayout()


        text_search_layout = QVBoxLayout()
        search_area = QLineEdit()
        search_area.setPlaceholderText("Buscar por firma o IP...")

        text_search_layout.addWidget(search_area)

        text_search = QWidget()
        text_search.setLayout(text_search_layout)
        text_search.setProperty( 'class', 'content_card' )


        severity_options_layout = QHBoxLayout()
        severity_options = QComboBox()
        severity_options.addItem(" Todas",0)
        severity_options.addItem(" Baja", 1)
        severity_options.addItem(" Media", 2)
        severity_options.addItem(" Alta", 3)
        severity_options.addItem(" Crítica",4)

        severity_options_layout.addWidget(severity_options)

        severity_filter = QWidget()
        severity_filter.setLayout(severity_options_layout)
        severity_filter.setProperty('class', 'content_card' )


        date_filter_layout = QHBoxLayout()
        date_options = QComboBox()
        date_options.addItem(" Últimas 24 horas", 0)
        date_options.addItem(" Últimas 48 horas", 1)
        date_options.addItem(" Últimos 7 días", 2)

        date_filter_layout.addWidget(date_options)

        date_filter = QWidget()
        date_filter.setLayout(date_filter_layout)
        date_filter.setProperty('class', 'content_card' )



        apply_filters_layout = QHBoxLayout()
        search_button = standard_button("Aplicar flitros", "./assets/search.svg")
        apply_filters_layout.addWidget(search_button)

        filters_layout.addWidget(text_search)
        filters_layout.addWidget(severity_filter)
        filters_layout.addWidget(date_filter)
        filters_layout.addStretch()
        filters_layout.addWidget(search_button)

        filters = QWidget()
        filters.setLayout(filters_layout)

        #layout principal de contenido
        alerts_main_layout = QHBoxLayout()

        alerts_container_layout = QVBoxLayout()
        title_container = QLabel('Lista de alertas')
        title_container.setProperty('class','card_title')
        alerts_list = QTableWidget()
        alerts_list.setColumnCount(4)
        alerts_list.setHorizontalHeaderLabels(
            ['Hora','Severidad','Firma','Origen']
        )
        alerts_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)



        alerts_container_layout.addWidget(title_container)
        alerts_container_layout.addWidget(alerts_list)


        alerts_container = QWidget()
        alerts_container.setLayout(alerts_container_layout)
        alerts_container.setProperty('class','content_card')

        alerts_details_layout = QVBoxLayout()
        title_details = QLabel('Detalles de la alerta')
        title_details.setProperty('class','card_title')





        alerts_details_layout.addWidget(title_details)
        alerts_details_layout.addStretch()
        alerts_details = QWidget()
        alerts_details.setLayout(alerts_details_layout)
        alerts_details.setProperty('class','content_card')
        alerts_details.setMinimumWidth(320)


        alerts_main_layout.addWidget(alerts_container)
        alerts_main_layout.addWidget(alerts_details)
        alerts_main = QWidget()
        alerts_main.setLayout(alerts_main_layout)


        layout.addWidget(title)
        layout.addWidget(filters)
        layout.addWidget(alerts_main)
        layout.addStretch()





        self.setLayout(layout)