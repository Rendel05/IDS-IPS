from PySide6 import QtCore
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

RED_CHART = './assets/red-chart.png'
GRAY_CHART = './assets/gray-chart.svg'
BLUE_CHART = './assets/blue-chart.svg'

PATHS = [RED_CHART,GRAY_CHART,BLUE_CHART]
COLORS = ['higher','equal','lower']

class TotalAlertsCard:
    def __init__(self,tab,data):
        super().__init__()
        self.tab = tab
        self.tab.setProperty('class', 'content_card')
        self.data = data


        critics_title = QLabel("Alertas Totales")
        critics_title.setProperty('class', 'card_title')

        self.critics_alerts_number = QLabel('')
        self.critics_alerts_number.setProperty('class', 'card_number')
        self.critics_alerts_number.setObjectName("card_number")
        self.critics_alerts_number.setContentsMargins(10,0,0,0)

        self.critics_alerts_percentage = QLabel('')
        self.critics_alerts_percentage.setProperty('class', 'card_percentage')
        self.critics_alerts_percentage.setObjectName("card_percentage")

        text_layout = QVBoxLayout()
        text_layout.addWidget(critics_title)
        text_layout.addWidget(self.critics_alerts_number)
        text_layout.addWidget(self.critics_alerts_percentage)

        self.critics_alerts_chart = QLabel()
        self.pixmap = QPixmap('')
        self.pixmap = self.pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.critics_alerts_chart.setPixmap(self.pixmap)

        self.main_layout = QHBoxLayout(self.tab)
        self.main_layout.addLayout(text_layout)
        self.main_layout.addWidget(self.critics_alerts_chart)

        self.refresh()

    def refresh(self, new_data = None):
        if new_data:
            self.data = new_data

        diff = self.data['yesterday_total'] - self.data['today_total']

        if diff < 0:
            diff_label = f'{abs(diff)} alertas más que ayer' if (abs(diff)) != 1 else f'{abs(diff)} alerta más que ayer'
            path = PATHS[0]
            color = COLORS[0]
        elif diff == 0:
            diff_label = 'Misma cantidad que ayer'
            path = PATHS[1]
            color = COLORS[1]
        else:
            diff_label = f'{diff} alertas menos que ayer' if diff != 1 else f'{diff} alerta menos que ayer'
            path = PATHS[2]
            color = COLORS[2]

        old_icon = self.critics_alerts_chart
        self.main_layout.removeWidget(old_icon)
        old_icon.deleteLater()
        self.critics_alerts_chart = QLabel()
        self.pixmap = QPixmap(path)
        self.pixmap = self.pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.critics_alerts_chart.setPixmap(self.pixmap)

        self.main_layout.addWidget(self.critics_alerts_chart)

        self.pixmap = QPixmap(path)
        self.critics_alerts_number.setText(f'{self.data['today_total']}')
        self.critics_alerts_number.setProperty('comparison', color)
        self.critics_alerts_number.style().unpolish(self.critics_alerts_number)
        self.critics_alerts_number.style().polish(self.critics_alerts_number)
        self.critics_alerts_percentage.setText(diff_label)
        self.critics_alerts_percentage.setProperty('comparison', color)
        self.critics_alerts_percentage.style().unpolish(self.critics_alerts_percentage)
        self.critics_alerts_percentage.style().polish(self.critics_alerts_percentage)


