from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget, QSizePolicy
from PySide6.QtCore import Qt

#:root{
LOW = '(172, 173, 184)'
MEDIUM = '(88, 166, 255)'
HIGH = '(210, 153, 34)'
CRITICAL = '(248, 81, 73)'

LOW_BG = '(172, 173, 184,51)'
MEDIUM_BG = '(88, 166, 255,51)'
HIGH_BG = '(210, 153, 34,51)'
CRITICAL_BG = '(248, 81, 73,51)'
# }

STATUS_MAPPER = {
    'crítica': 'critical',
    'critica': 'critical',
    'alta': 'high',
    'media': 'medium',
    'baja': 'low'
}


def mini_badge(text, status):
    status_en = STATUS_MAPPER.get(status.lower(), 'low')

    badge_layout = QHBoxLayout()
    badge_layout.setContentsMargins(0, 0, 0, 0)

    badge_text = QLabel(text)
    badge_text.setObjectName("badge_text")
    badge_text.setProperty('status', status_en)

    badge_layout.addWidget(badge_text)

    badge = QWidget()
    badge.setObjectName('badge')
    badge.setLayout(badge_layout)
    badge.setProperty('status', status_en)

    badge.setStyleSheet(f"""
        #badge[status = 'low'] {{
            background-color: rgba{LOW_BG};
            border: 1px solid rgb{LOW};
            border-radius: 10px;
        }}

        #badge_text[status = 'low'] {{
            color:rgb{LOW} ;
            font-weight: bold;
            font-size: 9px;
        }}

        #badge[status = 'medium'] {{
            background-color: rgba{MEDIUM_BG};
            border:1px solid rgb{MEDIUM};
            border-radius: 10px;
        }}

        #badge_text[status = 'medium'] {{
            color:rgb{MEDIUM} ;
            font-weight: bold;
            font-size: 9px;
        }}

        #badge[status = 'high'] {{
            background-color: rgba{HIGH_BG};
            border: 1px solid rgb{HIGH};
            border-radius: 10px;
        }}

        #badge_text[status = 'high'] {{
            color: rgb{HIGH};
            font-weight: bold;
            font-size: 9px;
        }}

        #badge[status = 'critical'] {{
            background-color: rgba{CRITICAL_BG};
            border:1px solid rgb{CRITICAL};
            border-radius: 10px;
        }}

        #badge_text[status = 'critical'] {{
            color: rgb{CRITICAL};
            font-weight: bold;
            font-size: 9px;
        }}

    """)

    badge.setFixedHeight(20)
    badge.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
    badge.setContentsMargins(10,0,10,0)

    container = QWidget()
    container_layout = QHBoxLayout(container)

    container_layout.addWidget(badge, alignment=Qt.AlignmentFlag.AlignCenter)
    container_layout.setContentsMargins(0,0,0,0)


    return container