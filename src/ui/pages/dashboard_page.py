from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTableWidget, \
    QHeaderView, QAbstractItemView, QSizePolicy

from services.database_manager import DatabaseManager
from ui.components.line_chart import LineChart
from ui.components.donut_chart import DonutChart
from ui.components.donut_label import DonutLabel
from ui.delegates.alerts_table_manager import RecentAlertsController
from ui.components.stats_tab import StatsCard


class DashboardPage(QWidget):
    def __init__(self,theme):
        super().__init__()
        layout = QVBoxLayout()
        self.db= DatabaseManager()


        #--------Título y subtítulo
        title_layout = QVBoxLayout()
        title_label = QLabel("Dashboard")
        title_label.setProperty('class', 'content_title')
        title_description = QLabel("Resumen general del estado del sistema.")
        title_description.setProperty('class', 'content_subtitle')
        title_layout.addWidget(title_label)
        title_layout.addWidget(title_description)

        title = QWidget()
        title.setLayout(title_layout)
        title.setFixedHeight(70)
        #--------------

        cards_layout = QHBoxLayout()

        #Layout de la tarjeta 'Alertas Totales'

        self.total_alerts = QWidget()
        #self.total_alerts_controller = TotalAlertsCard(self.total_alerts,self.db.get_alert_summary())
        self.total_alerts_controller = StatsCard(self.total_alerts,self.db.get_alert_summary(),'total')

        #Layout para la tarjeta 'Alertas Críticas'

        self.critics_alerts = QWidget()
        #self.critics_controller = CriticsAlertsCard(self.critics_alerts,self.db.get_alert_summary())
        self.critics_controller = StatsCard(self.critics_alerts,self.db.get_alert_summary(), 'critical')
        #--------------


        cards_layout.addWidget(self.total_alerts,stretch=35)
        cards_layout.addWidget(self.critics_alerts,stretch=35)
        cards_layout.addStretch(30)


        cards= QWidget()
        cards.setLayout(cards_layout)
        #--------------


        # Acá inician los organizadores gráficos
        #------------------------------------------------Gráfica de toro

        charts_layout = QHBoxLayout()

        donut_chart_layout = QVBoxLayout()
        donut_chart_title = QLabel('Porcentaje de alertas')
        donut_chart_title.setProperty('class', 'card_title')
        donut_chart_content_layout = QHBoxLayout()
        self.donut_chart = DonutChart(theme, self.db.get_chart_values())
        self.donut_labels = DonutLabel(self.db.get_chart_values())
        donut_chart_content_layout.addWidget(self.donut_chart)
        donut_chart_content_layout.addWidget(self.donut_labels)
        donut_chart_content=QWidget()
        donut_chart_content.setLayout(donut_chart_content_layout)
        donut_chart_layout.addWidget(donut_chart_title)
        donut_chart_layout.addWidget(donut_chart_content)

        donut_chart_widget = QWidget()
        donut_chart_widget.setLayout(donut_chart_layout)
        donut_chart_widget.setProperty('class', 'content_card')
        donut_chart_widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)


        #----------------------------------------------- gráfica de línea

        line_chart_layout = QVBoxLayout()
        line_chart_title = QLabel('Eventos en el tiempo')
        line_chart_title.setProperty('class','card_title')
        line_chart_content_layout = QHBoxLayout()
        self.line_chart = LineChart(theme, self.db.get_alerts_per_hour())
        line_chart_content_layout.addWidget(self.line_chart)

        line_chart_content = QWidget()
        line_chart_content.setLayout(line_chart_content_layout)

        line_chart_layout.addWidget(line_chart_title)
        line_chart_layout.addWidget(line_chart_content)
        line_chart_widget = QWidget()
        line_chart_widget.setLayout(line_chart_layout)
        line_chart_widget.setProperty('class', 'content_card')
        line_chart_widget.setFixedHeight(216)

        charts_layout.addWidget(donut_chart_widget, stretch=40)
        charts_layout.addWidget(line_chart_widget, stretch=60)
        charts = QWidget()
        charts.setLayout(charts_layout)
        charts.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        # --------------


        #Sección de alertas recientes
        recent_alerts_layout = QVBoxLayout()

        recent_alerts_title= QLabel('Alertas recientes')
        recent_alerts_title.setProperty('class', 'card_title')

        self.recent_alerts_table = QTableWidget()
        self.recent_alerts_table.setColumnCount(4)
        self.recent_alerts_table.setHorizontalHeaderLabels([
            'Hora', 'Severidad', 'Regla', 'Origen'])
        self.recent_alerts_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.recent_alerts_table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )
        self.recent_alerts_table.setObjectName('recent_alerts_table')
        self.recent_alerts_table.verticalHeader().setVisible(False)
        self.recent_alerts_table.setShowGrid(False)

        self.alert_controller = RecentAlertsController(
            self.recent_alerts_table, self.db
        )
        self.alert_controller.refresh()
        recent_alerts_layout.addWidget(recent_alerts_title)
        recent_alerts_layout.addWidget(self.recent_alerts_table)

        recent_alerts = QWidget()
        recent_alerts.setLayout(recent_alerts_layout)
        recent_alerts.setProperty('class', 'content_card')

        self.paging_layout = QHBoxLayout()

        paging = QWidget()
        paging.setLayout(self.paging_layout)


        #--------------
        layout.addWidget(title)
        layout.addWidget(cards)
        layout.addWidget(charts)
        layout.addWidget(recent_alerts)
        layout.addStretch()

        self.setLayout(layout)



    def change_theme(self, new_theme):
        self.donut_chart.update_theme(new_theme)
        self.line_chart.update_theme(new_theme)

    def refresh_data(self):
        self.db = DatabaseManager()

        self.total_alerts_controller.refresh(self.db.get_alert_summary())
        self.critics_controller.refresh(self.db.get_alert_summary())
        self.donut_chart.update_data(self.db.get_chart_values())
        self.donut_labels.refresh(self.db.get_chart_values())
        self.line_chart.update_data(self.db.get_alerts_per_hour())
        self.alert_controller.refresh()