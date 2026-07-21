from PySide6.QtGui import Qt
from PySide6.QtWidgets import QLabel, QWidget

from services.database_manager import DatabaseManager
from ui.components.badges import badges
from services.date_normalizer import normalize_timestamp


class AlertDetails:
    ALERT_DESCRIPTIONS = {
        "ICMP Flood": (
            "Se detectó un volumen inusual de paquetes ICMP. "
            "Verifique el origen del tráfico y confirme que no se trate de una prueba o ataque de red."
        ),

        "Sniffer": (
            "Se identificó una interfaz en modo promiscuo. "
            "Revise los procesos activos y confirme que no exista software de captura no autorizado."
        ),

        "Port Scan": (
            "Se detectó actividad compatible con un escaneo de puertos. "
            "Compruebe el origen y determine si corresponde a una auditoría autorizada."
        ),

        "Beaconing": (
            "El dispositivo está realizando comunicaciones periódicas hacia un mismo destino. "
            "Valide la legitimidad de la conexión y supervise su comportamiento."
        ),

        "IP Change": (
            "Se detectó una reasignación de dirección IP. "
            "Verifique que el cambio sea esperado y que no existan conflictos en la red."
        ),

        "ip change": (
            "Se detectó una reasignación de dirección IP. "
            "Verifique que el cambio sea esperado y que no existan conflictos en la red."
        ),

        "New Port Open": (
            "Se identificó la apertura de un nuevo puerto de red. "
            "Confirme qué servicio lo utiliza y si su exposición es necesaria."
        ),

        "New Device": (
            "Se detectó la activación de un periférico de captura de audio o video. "
            "Compruebe que el dispositivo y la aplicación que lo utiliza sean legítimos."
        )
    }

    def __init__(self, layout=None):
        self.layout = layout
        self.current_alert_id=0

        self.severity_label = QLabel('<strong>Severidad:</strong>')
        self.severity_badge = QWidget()

        self.rule_label = QLabel('<strong>Firma/Regla:</strong>')
        self.rule = QLabel('')
        self.rule.setWordWrap(True)
        self.rule.setTextInteractionFlags(
            Qt.TextSelectableByMouse |
            Qt.TextSelectableByKeyboard
        )
        self.description_label = QLabel('<strong>Descripción:</strong>')
        self.description = QLabel('')
        self.description.setWordWrap(True)
        self.description.setTextInteractionFlags(
            Qt.TextSelectableByMouse |
            Qt.TextSelectableByKeyboard
        )
        self.source_label = QLabel('<strong>Origen/Destino:</strong>')
        self.source = QLabel('')
        self.source.setWordWrap(True)
        self.source.setTextInteractionFlags(
            Qt.TextSelectableByMouse |
            Qt.TextSelectableByKeyboard
        )
        self.date_label = QLabel('<strong>Fecha y hora:</strong>')
        self.date = QLabel('')
        self.date.setWordWrap(True)
        self.date.setTextInteractionFlags(
            Qt.TextSelectableByMouse |
            Qt.TextSelectableByKeyboard
        )
        self.advice_label = QLabel('<strong>Información adicional:</strong>')
        self.advice = QLabel('')
        self.advice.setWordWrap(True)
        self.advice.setTextInteractionFlags(
            Qt.TextSelectableByMouse |
            Qt.TextSelectableByKeyboard
        )

        self.layout.addWidget(self.severity_label)
        self.layout.addWidget(self.severity_badge)
        self.layout.addWidget(self.rule_label)
        self.layout.addWidget(self.rule)
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description)
        self.layout.addWidget(self.source_label)
        self.layout.addWidget(self.source)
        self.layout.addWidget(self.date_label)
        self.layout.addWidget(self.date)
        self.layout.addWidget(self.advice_label)
        self.layout.addWidget(self.advice)

    def refresh(self,alert_id :int):
        if self.current_alert_id == alert_id:
            return
        data = DatabaseManager().get_alert_details(alert_id)

        valid_rules = ("ICMP Flood", "Sniffer", "Port Scan", "Beaconing")
        real_source = data[4].split()[-1] if data[3] in valid_rules else "---"


        old_badge = self.severity_badge
        self.layout.removeWidget(old_badge)
        old_badge.deleteLater()
        self.severity_badge = badges(data[2], data[2])

        self.layout.insertWidget(2, self.severity_badge)
        self.rule.setText(f'{data[3]}')
        self.description.setText(f'{data[4]}')
        self.source.setText(real_source)
        self.date.setText(f'{normalize_timestamp(data[1])}')
        self.advice.setText(self.ALERT_DESCRIPTIONS.get(data[3]))

        self.current_alert_id = alert_id
