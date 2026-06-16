from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout, QTableWidget, QTableWidgetItem, \
    QHeaderView, QAbstractItemView, QSizePolicy
from PySide6.QtCore import Qt, QSize
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

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
    def __init__(self):
        super().__init__()
        layout = QGridLayout()

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
        #total_alerts.setFixedHeight(130)
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
        #events.setFixedHeight(130)
        #--------------

        #Acá inician los organizadores gráficos
        #Gráfica de pastel
        circular_chart_layout = QVBoxLayout()

        circular_chart_title = QLabel("Alertas por severidad")
        circular_chart_title.setProperty('class', 'card_title')

        chart1 = Figure()
        canvas1 = FigureCanvasQTAgg(chart1)
        canvas1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas1.setMinimumSize(QSize(100, 100))

        circular_chart_layout.addWidget(circular_chart_title)
        circular_chart_layout.addWidget(canvas1)

        circular_chart = QWidget()
        circular_chart.setLayout(circular_chart_layout)
        circular_chart.setProperty('class', 'content_card')
        circular_chart.setFixedSize(278,220)


        #Histograma en vivo
        histogram_chart_layout = QVBoxLayout()

        histogram_chart_title = QLabel('Volumen de descarga en vivo')
        histogram_chart_title.setProperty('class', 'card_title')

        chart2 = Figure()
        canvas2 = FigureCanvasQTAgg(chart2)
        canvas2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas2.setMinimumSize(QSize(100, 100))

        histogram_chart_layout.addWidget(histogram_chart_title)
        histogram_chart_layout.addWidget(canvas2)

        histogram_chart = QWidget()
        histogram_chart.setLayout(histogram_chart_layout)
        histogram_chart.setProperty('class', 'content_card')
        histogram_chart.setMaximumHeight(220)

        #--------------


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

        layout.addWidget(title,0,0)

        layout.addWidget(total_alerts,1,0)
        layout.addWidget(critics_alerts,1,1)
        layout.addWidget(events,1,2)

        layout.addWidget(circular_chart,2,0,1,1)
        layout.addWidget(histogram_chart,2,1,1,2)

        layout.addWidget(recent_alerts,3,0,1,3)



        self.setLayout(layout)

#        circular_chart.setMinimumWidth(288)       circular_chart.setMaximumWidth(288)