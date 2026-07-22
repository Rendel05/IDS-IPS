from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.path_resolver import resource_path


ICON_PATHS = {
    "info": resource_path("src/assets/information-circle.svg"),
    "success": resource_path("src/assets/check-circle.svg"),
    "warning": resource_path("src/assets/exclamation-triangle.svg"),
    "danger": resource_path("src/assets/x-circle.svg"),
}

class SweetAlert:

    def __init__(
        self,
        parent=None,
        title="",
        text="",
        icon="warning",
        confirm_text="Confirmar",
        cancel_text="Cancelar",
        show_cancel=True,
    ):
        self._result = False

        self.dialog = QDialog(parent)
        self.dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.dialog.setAttribute(Qt.WA_TranslucentBackground)
        self.dialog.setModal(True)
        self.dialog.setMinimumWidth(360)
        self.dialog.setObjectName("sweetAlert")

        icon_path = ICON_PATHS.get(icon, ICON_PATHS["info"])

        card = QWidget(self.dialog)
        card.setObjectName("sweetAlertCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 25)
        card_layout.setSpacing(12)
        card_layout.setAlignment(Qt.AlignCenter)

        shadow = QGraphicsDropShadowEffect(self.dialog)
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 150))
        card.setGraphicsEffect(shadow)

        icon_label = QLabel()
        icon_label.setObjectName("sweetAlertIcon")
        icon_label.setProperty("type", icon)
        icon_label.setScaledContents(True)
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            icon_label.setPixmap(pixmap)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        title_label.setObjectName("sweetAlertTitle")

        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        text_label.setObjectName("sweetAlertText")

        button_row = QHBoxLayout()
        button_row.setSpacing(10)
        button_row.setAlignment(Qt.AlignCenter)

        confirm_button = QPushButton(confirm_text)
        confirm_button.setCursor(Qt.PointingHandCursor)
        confirm_button.setFixedHeight(38)
        confirm_button.setObjectName("sweetAlertConfirmButton")
        confirm_button.setProperty("type", icon)
        confirm_button.clicked.connect(self._on_confirm)
        button_row.addWidget(confirm_button)

        if show_cancel:
            cancel_button = QPushButton(cancel_text)
            cancel_button.setCursor(Qt.PointingHandCursor)
            cancel_button.setFixedHeight(38)
            cancel_button.setObjectName("sweetAlertCancelButton")
            cancel_button.clicked.connect(self._on_cancel)
            button_row.addWidget(cancel_button)

        card_layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        card_layout.addWidget(title_label)
        if text:
            card_layout.addWidget(text_label)
        card_layout.addSpacing(10)
        card_layout.addLayout(button_row)

        outer_layout = QVBoxLayout(self.dialog)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(card)

    def _on_confirm(self):
        self._result = True
        self.dialog.accept()

    def _on_cancel(self):
        self._result = False
        self.dialog.reject()

    def exec(self):
        self.dialog.exec()
        return self._result

    @classmethod
    def confirm(
        cls,
        parent=None,
        title="¿Estás seguro?",
        text="",
        icon="warning",
        confirm_text="Sí, continuar",
        cancel_text="Cancelar",
    ):
        instance = cls(
            parent=parent,
            title=title,
            text=text,
            icon=icon,
            confirm_text=confirm_text,
            cancel_text=cancel_text,
            show_cancel=True,
        )
        return instance.exec()

    @classmethod
    def alert(
        cls,
        parent=None,
        title="",
        text="",
        icon="info",
        confirm_text="Aceptar",
    ):
        instance = cls(
            parent=parent,
            title=title,
            text=text,
            icon=icon,
            confirm_text=confirm_text,
            show_cancel=False,
        )
        return instance.exec()