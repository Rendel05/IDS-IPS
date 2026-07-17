from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

RED_CHART = './assets/red-chart.png'
GRAY_CHART = './assets/gray-chart.svg'
BLUE_CHART = './assets/blue-chart.svg'

PATHS = [RED_CHART, GRAY_CHART, BLUE_CHART]
COLORS = ['higher', 'equal', 'lower']


class StatsCard:
    CONFIG = {
        'critical': {
            'title': 'Alertas Graves',
            'key_yesterday': 'yesterday_high_critical',
            'key_today': 'today_high_critical'
        },
        'total': {
            'title': 'Alertas Totales',
            'key_yesterday': 'yesterday_total',
            'key_today': 'today_total'
        }
    }

    def __init__(self, tab, data, card_type='critical'):
        super().__init__()

        self.tab = tab
        self.tab.setProperty('class', 'content_card')
        self.data = data
        self.card_config = self.CONFIG[card_type]

        card_title = QLabel(self.card_config['title'])
        card_title.setProperty('class', 'card_title')

        self.alerts_number = QLabel('')
        self.alerts_number.setProperty('class', 'card_number')
        self.alerts_number.setObjectName("card_number")
        self.alerts_number.setContentsMargins(10, 0, 0, 0)

        self.alerts_percentage = QLabel('')
        self.alerts_percentage.setProperty('class', 'card_percentage')
        self.alerts_percentage.setObjectName("card_percentage")

        text_layout = QVBoxLayout()
        text_layout.addWidget(card_title)
        text_layout.addWidget(self.alerts_number)
        text_layout.addWidget(self.alerts_percentage)

        self.alerts_chart = QLabel()
        self.main_layout = QHBoxLayout(self.tab)
        self.main_layout.addLayout(text_layout)
        self.main_layout.addWidget(self.alerts_chart)

        self.refresh()

    def refresh(self, new_data=None):
        if new_data:
            self.data = new_data

        key_yesterday = self.card_config['key_yesterday']
        key_today = self.card_config['key_today']

        diff = self.data[key_yesterday] - self.data[key_today]

        if diff < 0:
            diff_label = f'{abs(diff)} alertas más que ayer' if abs(diff) != 1 else f'{abs(diff)} alerta más que ayer'
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

        self.main_layout.removeWidget(self.alerts_chart)
        self.alerts_chart.deleteLater()

        self.alerts_chart = QLabel()
        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.alerts_chart.setPixmap(pixmap)
        self.main_layout.addWidget(self.alerts_chart)

        self.alerts_number.setText(f"{self.data[key_today]}")
        self.alerts_number.setProperty('comparison', color)
        self.alerts_number.style().unpolish(self.alerts_number)
        self.alerts_number.style().polish(self.alerts_number)

        self.alerts_percentage.setText(diff_label)
        self.alerts_percentage.setProperty('comparison', color)
        self.alerts_percentage.style().unpolish(self.alerts_percentage)
        self.alerts_percentage.style().polish(self.alerts_percentage)