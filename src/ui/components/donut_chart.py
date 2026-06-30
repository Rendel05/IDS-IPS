from PySide6.QtCore import QSize
from PySide6.QtWidgets import QSizePolicy

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.patches import Wedge



class DonutChart(FigureCanvasQTAgg):
    COLORS = [
        "#F85149",  # Crítica
        "#E3A533",  # Alta
        "#4A7DFF",  # Media
        "#586B95",  # Baja
    ]

    def __init__(self, theme,values):
        self.theme = theme
        self.current_values = values
        #self.current_values = [10,20,30,40]
        self.text_color = '#5A6472' if self.theme == "dark" else "#99A2AB"

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

        if sum(values) == 0:
            ring = Wedge(
                center=(0, 0),
                r=1.0,
                theta1=0,
                theta2=360,
                width=0.35,
                facecolor="#353535",
                edgecolor=self.theme,
                linewidth=2,
            )
            self.ax.add_patch(ring)
            self.ax.set_xlim(-1.2, 1.2)
            self.ax.set_ylim(-1.2, 1.2)
        else:
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