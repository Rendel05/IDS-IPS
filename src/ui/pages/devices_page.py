from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class DevicesPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        title_label = QLabel("Dispositivos")
        title_label.setProperty('class', 'content_title')
        title_description = QLabel("Gestión y consulta de dispositivos periféricos del equipo.")
        title_description.setProperty('class', 'content_subtitle')
        title_layout.addWidget(title_label)
        title_layout.addWidget(title_description)

        title = QWidget()
        title.setLayout(title_layout)
        title.setFixedHeight(70)

        layout.addWidget(title)
        layout.addStretch()

        self.setLayout(layout)