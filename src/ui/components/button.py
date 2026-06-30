from PySide6.QtWidgets import QPushButton,QSizePolicy

def standard_button(text , path= None):
    
    button = QPushButton(text)
    button.setObjectName("standard_button")

    button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    return button