from PySide6.QtCore import QSize
from PySide6.QtWidgets import QSizePolicy

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


class DonutChart(FigureCanvasQTAgg):
    COLORS = [
        "#F85149",  # Crítica
        "#E3A533",  # Alta
        "#4A7DFF",  # Media
        "#586B95",  # Baja
    ]

    def __init__(self, theme):
        self.theme = theme
        self.current_values = [10, 20, 30, 40]

        self.figure = Figure(facecolor="none")
        super().__init__(self.figure)

        self.ax = self.figure.add_axes([0.05, 0.05, 0.90, 0.90])

        self.setStyleSheet("background: transparent;")
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.update_data(self.current_values)

    def sizeHint(self):
        return QSize(160, 160)

    def minimumSizeHint(self):
        return QSize(120, 120)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = self.width() / self.figure.dpi
        h = self.height() / self.figure.dpi
        self.figure.set_size_inches(w, h, forward=False)
        self.draw_idle()

    def update_theme(self, new_theme):
        self.theme = new_theme
        self.update_data(self.current_values)

    def update_data(self, values):
        self.current_values = values
        self.ax.clear()
        self.ax.set_facecolor("none")
        self.ax.axis("off")

        self.ax.pie(
            self.current_values,
            colors=self.COLORS,
            startangle=90,
            counterclock=False,
            wedgeprops={
                "width": 0.35,
                "linewidth": 2,
                "edgecolor": self.theme,
            },
        )

        self.draw_idle()