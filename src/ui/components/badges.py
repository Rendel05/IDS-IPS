from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget, QSizePolicy

#:root{
LOW = '(172, 173, 184)'
MEDIUM = '(88, 166, 255)'
HIGH = '(210, 153, 34)'
CRITICAL ='(248, 81, 73)'

LOW_BG = '(172, 173, 184,51)'
MEDIUM_BG = '(88, 166, 255,51)'
HIGH_BG = '(210, 153, 34,51)'
CRITICAL_BG = '(248, 81, 73,51)'

# }

def badges(text,status):
    badge_layout = QHBoxLayout()

    badge_text = QLabel(text)
    badge_text.setObjectName("badge_text")
    badge_text.setProperty('status',status)

    badge_layout.addWidget(badge_text)

    badge = QWidget()
    badge.setObjectName('badge')
    badge.setLayout(badge_layout)
    badge.setProperty('status',status)


    badge.setStyleSheet(f"""
        #badge[status = 'low'] {{
            background-color: rgba{LOW_BG};
            border-color: rgb{LOW};
            border-radius: 15px;
        }}
        
        #badge_text[status = 'low'] {{
            color:rgb{LOW} ;
            font-weight: bold;
        }}
        
        #badge[status = 'medium'] {{
            background-color: rgba{MEDIUM_BG};
            border-color: rgb{MEDIUM};
            border-radius: 15px;
        }}
        
        #badge_text[status = 'medium'] {{
            color:rgb{MEDIUM} ;
            font-weight: bold;
        }}
        
        #badge[status = 'high'] {{
            background-color: rgba{HIGH_BG};
            border-color: rgb{HIGH};
            border-radius: 15px;
        }}
        
        #badge_text[status = 'high'] {{
            color: rgb{HIGH};
            font-weight: bold;
        }}
        
        #badge[status = 'critical'] {{
            
            background-color: rgba{CRITICAL_BG};
            border-color: rgb{CRITICAL};
            border-radius: 15px;
        }}
        
        #badge_text[status = 'critical'] {{
            color: rgb{CRITICAL};
            font-weight: bold;
        }}
        #badge{{
            padding: 2px 8px;  
        }}
    """)
    badge.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    return badge


