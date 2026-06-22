from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout, QTableWidget, QTableWidgetItem, \
    QHeaderView, QAbstractItemView, QSizePolicy
from PySide6.QtCore import Qt

from ui.components.donut_chart import DonutChart
from ui.components.donut_label import DonutLabel

#int
TOTAL_ALERTS = 0
CRITICS_ALERTS = 100
TOTAL_EVENTS = -1000
#%
TOTAL_PERCENTAGE = 0
CRITICS_PERCENTAGE = 75
EVENTS_PERCENTAGE = -50

RED_CHART = './assets/red-chart.png'
BLUE_CHART = './assets/blue-chart.svg'
GRAY_CHART = './assets/gray-chart.svg'

def set_color(n):
    if n < 0:
        return'lower'
    elif n == 0:
        return 'equal'
    else:
        return 'higher'

def set_path(n):
    if n < 0:
        return './assets/blue-chart.svg'
    elif n == 0:
        return './assets/gray-chart.svg'
    else:
        return './assets/red-chart.png'



class DashboardPage(QWidget):
    def __init__(self,theme):
        super().__init__()
        layout = QVBoxLayout()
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

        cards_layout = QGridLayout()

        #Layout de la tarjeta 'Alertas Totales'
        total_alerts_layout = QHBoxLayout()

        total_alerts_text_layout = QVBoxLayout()
        total_alerts_title= QLabel("Alertas Totales")
        total_alerts_title.setProperty('class', 'card_title')
        total_alerts_number = QLabel(f'{TOTAL_ALERTS}')
        total_alerts_number.setProperty('class', 'card_number')
        total_alerts_number.setObjectName("card_number")
        total_alerts_number.setProperty('comparison', set_color(TOTAL_ALERTS))
        total_alerts_percentage = QLabel(f'{TOTAL_PERCENTAGE}% vs ayer')
        total_alerts_percentage.setProperty('class', 'card_percentage')
        total_alerts_percentage.setObjectName("card_percentage")
        total_alerts_percentage.setProperty('comparison', set_color(TOTAL_PERCENTAGE))
        total_alerts_text_layout.addWidget(total_alerts_title)
        total_alerts_text_layout.addWidget(total_alerts_number)
        total_alerts_text_layout.addWidget(total_alerts_percentage)

        total_alerts_text = QWidget()
        total_alerts_text.setLayout(total_alerts_text_layout)

        chart_alerts_layout = QVBoxLayout()

        total_alerts_chart = QLabel()
        pixmap1 = QPixmap(set_path(TOTAL_PERCENTAGE))
        pixmap1 = pixmap1.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        total_alerts_chart.setPixmap(pixmap1)
        chart_alerts_layout.addWidget(total_alerts_chart)

        chart_alerts = QWidget()
        chart_alerts.setLayout(chart_alerts_layout)

        total_alerts_layout.addWidget(total_alerts_text)
        total_alerts_layout.addWidget(total_alerts_chart)

        total_alerts = QWidget()
        total_alerts.setLayout(total_alerts_layout)
        total_alerts.setProperty('class','content_card')
        #--------------


        #Layout para la tarjeta 'Alertas Críticas'
        critics_alerts_layout = QHBoxLayout()

        critics_alerts_text_layout = QVBoxLayout()
        critics_title = QLabel("Alertas Críticas")
        critics_title.setProperty('class', 'card_title')
        critics_alerts_number = QLabel(f'{CRITICS_ALERTS}')
        critics_alerts_number.setProperty('class', 'card_number')
        critics_alerts_number.setObjectName("card_number")
        critics_alerts_number.setProperty('comparison', set_color(CRITICS_ALERTS))
        critics_alerts_percentage = QLabel(f'{CRITICS_PERCENTAGE}% vs ayer')
        critics_alerts_percentage.setProperty('class', 'card_percentage')
        critics_alerts_percentage.setObjectName("card_percentage")
        critics_alerts_percentage.setProperty('comparison', set_color(CRITICS_PERCENTAGE))
        critics_alerts_text_layout.addWidget(critics_title)
        critics_alerts_text_layout.addWidget(critics_alerts_number)
        critics_alerts_text_layout.addWidget(critics_alerts_percentage)

        critics_alerts_text = QWidget()
        critics_alerts_text.setLayout(critics_alerts_text_layout)

        critics_icon_layout = QHBoxLayout()

        critics_alerts_chart = QLabel()
        pixmap2 = QPixmap(set_path(CRITICS_PERCENTAGE))
        pixmap2 = pixmap2.scaled(120,120,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        critics_alerts_chart.setPixmap(pixmap2)
        critics_icon_layout.addWidget(critics_alerts_chart)

        critics_icon = QWidget()
        critics_icon.setLayout(critics_icon_layout)

        critics_alerts_layout.addWidget(critics_alerts_text)
        critics_alerts_layout.addWidget(critics_icon)

        critics_alerts = QWidget()
        critics_alerts.setLayout(critics_alerts_layout)
        critics_alerts.setProperty('class', 'content_card')
        #critics_alerts.setFixedHeight(130)
        #--------------

        #Layout para la tarjeta 'Todos los eventos'
        events_layout = QHBoxLayout()

        events_text_layout = QVBoxLayout()
        events_title = QLabel("Todos de eventos")
        events_title.setProperty('class', 'card_title')
        events_title_number = QLabel(f'{TOTAL_EVENTS}')
        events_title_number.setProperty('class', 'card_number')
        events_title_number.setObjectName("card_number")
        events_title_number.setProperty('comparison', set_color(TOTAL_EVENTS))
        events_percentage = QLabel(f'{EVENTS_PERCENTAGE}% vs ayer')
        events_percentage.setProperty('class', 'card_percentage')
        events_percentage.setObjectName("card_percentage")
        events_percentage.setProperty('comparison', set_color(EVENTS_PERCENTAGE))
        events_text_layout.addWidget(events_title)
        events_text_layout.addWidget(events_title_number)
        events_text_layout.addWidget(events_percentage)

        events_text = QWidget()
        events_text.setLayout(events_text_layout)

        chart_events_layout = QHBoxLayout()

        events_chart = QLabel()
        pixmap3 = QPixmap(set_path(EVENTS_PERCENTAGE))
        pixmap3 = pixmap3.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        events_chart.setPixmap(pixmap3)

        chart_events_layout.addWidget(events_chart)

        chart_events = QWidget()
        chart_events.setLayout(chart_events_layout)

        events_layout.addWidget(events_text)
        events_layout.addWidget(chart_events)

        events = QWidget()
        events.setLayout(events_layout)
        events.setProperty('class', 'content_card')


        cards_layout.addWidget(total_alerts,0,0)
        cards_layout.addWidget(critics_alerts,0,1)
        cards_layout.addWidget(events,0,2)

        cards= QWidget()
        cards.setLayout(cards_layout)
        #--------------



        # Acá inician los organizadores gráficos
        # Gráfica de toro

        charts_layout = QHBoxLayout()

        donut_chart_layout = QVBoxLayout()
        donut_chart_title = QLabel('Porcentaje de alertas')
        donut_chart_title.setProperty('class', 'card_title')
        donut_chart_content_layout = QHBoxLayout()
        self.donut_chart = DonutChart(theme)
        donut_labels = DonutLabel()
        donut_chart_content_layout.addWidget(self.donut_chart)
        donut_chart_content_layout.addWidget(donut_labels)
        donut_chart_content=QWidget()
        donut_chart_content.setLayout(donut_chart_content_layout)
        donut_chart_layout.addWidget(donut_chart_title)
        donut_chart_layout.addWidget(donut_chart_content)

        donut_chart_widget = QWidget()
        donut_chart_widget.setLayout(donut_chart_layout)
        donut_chart_widget.setProperty('class', 'content_card')


        #----------------------------------------------- gráfica de línea
        line_chart_layout = QVBoxLayout()
        line_chart_widget = QWidget()
        line_chart_widget.setLayout(line_chart_layout)
        line_chart_widget.setProperty('class', 'content_card')


        charts_layout.addWidget(donut_chart_widget, stretch=45)
        charts_layout.addWidget(line_chart_widget, stretch=55)
        charts = QWidget()
        charts.setLayout(charts_layout)
        # --------------


        #Sección de alertas recientes
        recent_alerts_layout = QVBoxLayout()

        recent_alerts_title= QLabel('Alertas recientes')
        recent_alerts_title.setProperty('class', 'card_title')

        recent_alerts_table = QTableWidget()
        recent_alerts_table.setColumnCount(4)
        recent_alerts_table.setRowCount(6)
        recent_alerts_table.setHorizontalHeaderLabels([
            'Hora', 'Severidad', 'Regla', 'Origen'])
        recent_alerts_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        recent_alerts_table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )
        recent_alerts_table.setObjectName('recent_alerts_table')
        recent_alerts_table.verticalHeader().setVisible(False)
        recent_alerts_table.setShowGrid(False)
        recent_alerts_layout.addWidget(recent_alerts_title)
        recent_alerts_layout.addWidget(recent_alerts_table)

        recent_alerts = QWidget()
        recent_alerts.setLayout(recent_alerts_layout)
        recent_alerts.setProperty('class', 'content_card')


        #--------------
        layout.addWidget(title)
        layout.addWidget(cards)
        layout.addWidget(charts)
        layout.addWidget(recent_alerts)

        self.setLayout(layout)

    def change_theme(self, new_theme):
        self.donut_chart.update_theme(new_theme)