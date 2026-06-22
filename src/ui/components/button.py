from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton,QSizePolicy

def standard_button(text , path= None):
    
    button = QPushButton(text)
    button.setObjectName("standard_button")

    if path is not None:
        button.setIcon(QIcon(path))

    button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    return button