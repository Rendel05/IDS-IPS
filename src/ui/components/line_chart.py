from PySide6.QtCore import QSize
from PySide6.QtWidgets import QSizePolicy

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


class LineChart(FigureCanvasQTAgg):
    def __init__(self, theme, data):
        self.theme = theme
        self.current_data = data

        self.figure = Figure(facecolor="none")
        super().__init__(self.figure)

        self.ax = self.figure.add_axes([0.08, 0.12, 0.89, 0.78])

        for spine in self.ax.spines.values():
            spine.set_visible(False)

        self.setStyleSheet("background: transparent;")
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.update_data(data)

    def sizeHint(self):
        return QSize(400, 200)

    def minimumSizeHint(self):
        return QSize(250, 150)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        w = self.width() / self.figure.dpi
        h = self.height() / self.figure.dpi

        self.figure.set_size_inches(w, h, forward=False)
        self.draw_idle()

    def update_theme(self, new_theme):
        self.theme = new_theme
        self.update_data(self.current_data)

    def update_data(self, data):
        self.current_data = data


        self.ax.clear()
        self.ax.set_facecolor("none")

        text_color  = "#6B7A8D" if self.theme == "#13171f" else "#99A2AB"
        line_color  = "#4A7DFF"
        dot_color   = "#4A7DFF"
        grid_color  = "#2A3142" if self.theme == "#13171f" else "#99A2AB"
        fill_top    = "#4A7DFF22"
        fill_bottom = "#4A7DFF00"

        hours  = sorted(data.keys())
        values = [data[hour] for hour in hours]
        all_zero = not values or max(values) == 0

        if all_zero:
            tick_hours = list(range(0, 24, 4)) + [23]
            tick_labels = [f"{h:02d}:00" for h in range(0, 24, 4)] + ["24:00"]

            self.ax.set_xticks(tick_hours)
            self.ax.set_xticklabels(tick_labels, color=text_color, fontsize=8)
            self.ax.set_xlim(-0.5, 23.5)

            self.ax.set_ylim(0, 1)

            self.ax.set_yticks([])

            self.ax.yaxis.grid(False)
            self.ax.xaxis.grid(False)

            self.ax.text(
                11.5,
                0.5,
                "Sin eventos registrados",
                ha="center",
                va="center",
                fontsize=10,
                color=text_color,
                alpha=0.75,
            )

            self.draw_idle()
            return


        self.ax.plot(
            hours,
            values,
            color=line_color,
            linewidth=1.8,
            solid_capstyle="round",
            solid_joinstyle="round",
            zorder=3,
        )

        self.ax.fill_between(
            hours, values,
            alpha=0.18,
            color=line_color,
            linewidth=0,
            zorder=2,
        )
        self.ax.fill_between(
            hours, values,
            alpha=0.06,
            color=line_color,
            linewidth=0,
            zorder=1,
        )

        self.ax.scatter(
            hours,
            values,
            color=dot_color,
            s=28,
            zorder=4,
            linewidths=0,
        )

        tick_hours  = list(range(0, 24, 4)) + [23]
        tick_labels = [f"{h:02d}:00" for h in range(0, 24, 4)] + ["24:00"]

        self.ax.set_xticks(tick_hours)
        self.ax.set_xticklabels(tick_labels, color=text_color, fontsize=8)
        self.ax.set_xlim(-0.5, 23.5)

        max_val = max(values) if values else 1
        y_top   = max_val * 1.25

        def y_formatter(val, _):
            if val >= 1000:
                return f"{int(val / 1000)}K"
            return str(int(val)) if val == int(val) else ""

        self.ax.yaxis.set_major_formatter(
            __import__("matplotlib.ticker", fromlist=["FuncFormatter"]).FuncFormatter(y_formatter)
        )
        self.ax.set_ylim(0, y_top)
        self.ax.tick_params(axis="y", colors=text_color, labelsize=8)

        self.ax.set_xlabel("")
        self.ax.set_ylabel("")

        self.ax.tick_params(axis="both", length=0)

        self.ax.yaxis.grid(True, color=grid_color, linewidth=0.7, linestyle="-")
        self.ax.xaxis.grid(False)
        self.ax.set_axisbelow(True)

        for spine in self.ax.spines.values():
            spine.set_visible(False)

        self.draw_idle()