from PySide6.QtWidgets import QAbstractButton
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, Property


class CustomSwitch(QAbstractButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedSize(60, 30)
        self._thumb_position = 3

    @Property(int)
    def thumb_position(self):
        return self._thumb_position

    @thumb_position.setter
    def thumb_position(self, pos):
        self._thumb_position = pos
        self.update()

    def nextCheckState(self):
        super().nextCheckState()
        ani = QPropertyAnimation(self, b"thumb_position", self)
        ani.setDuration(120)
        if self.isChecked():
            ani.setEndValue(33)
        else:
            ani.setEndValue(3)
        ani.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        bg_color = QColor("#2ECC71") if self.isChecked() else QColor("#BDC3C7")
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)

        painter.drawRoundedRect(0, 0, self.width(), self.height(), 15, 15)

        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(self._thumb_position, 3, 24, 24)