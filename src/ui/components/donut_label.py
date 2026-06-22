from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QGridLayout



class DonutLabel(QWidget):

    def __init__(self):

        super().__init__()

        COLORS = [
            "#F85149",  # Crítica
            "#E3A533",  # Alta
            "#4A7DFF",  # Media
            "#586B95"  # Baja
        ]
        TAGS = [
            "Crítica",
            "Alta",
            "Media",
            "Baja"
        ]
        #Acá se mandará a llamar a otra función que calcule los porcentajes, valores de prueba
        number = ['(10%)', '(20%)', '(30%)', '(40%)']

        layout = QGridLayout()

        for row, (color, tag, percentage) in enumerate(
                zip(COLORS, TAGS, number)
        ):
            color_label = QLabel('■')
            color_label.setStyleSheet(f"color:{color};")
            color_label.setMaximumWidth(10)

            tag_label = QLabel(tag)
            tag_label.setObjectName('chart_tag')

            percentage_label = QLabel(percentage)
            percentage_label.setContentsMargins(40, 0, 0, 0)


            layout.addWidget(color_label, row, 0)
            layout.addWidget(tag_label, row, 1)
            layout.addWidget(percentage_label, row, 2)

        self.setLayout(layout)

