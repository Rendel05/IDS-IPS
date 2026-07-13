from PySide6.QtWidgets import QLabel, QWidget, QGridLayout


class DonutLabel(QWidget):
    COLORS = [
        "#F85149",  # Crítica
        "#E3A533",  # Alta
        "#4A7DFF",  # Media
        "#586B95",  # Baja
    ]

    TAGS = [
        "Crítica",
        "Alta",
        "Media",
        "Baja"
    ]

    def __init__(self, initial_values):
        super().__init__()

        layout = QGridLayout()
        layout.setContentsMargins(0, 25, 0, 25)


        self.percentage_labels = []

        for row, (color, tag) in enumerate(zip(self.COLORS, self.TAGS)):
            color_label = QLabel('■')
            color_label.setStyleSheet(f"color: {color};")
            color_label.setMaximumWidth(10)

            tag_label = QLabel(tag)
            tag_label.setObjectName('chart_tag')

            p_label = QLabel()
            p_label.setContentsMargins(40, 0, 0, 0)
            self.percentage_labels.append(p_label)

            layout.addWidget(color_label, row, 0)
            layout.addWidget(tag_label, row, 1)
            layout.addWidget(p_label, row, 2)

        self.setLayout(layout)

        self.refresh(initial_values)

    def refresh(self, values):

        total = sum(values)

        for i, val in enumerate(values):
            if total > 0:
                percentage = (val * 100) / total
            else:
                percentage = 0.0

            self.percentage_labels[i].setText(f"({percentage:.0f}%)")