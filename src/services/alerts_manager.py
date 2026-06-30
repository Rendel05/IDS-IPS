from datetime import datetime


class AlertManager:

    def __init__(self, db):
        self.db = db

    def create_alert(self, severity, category, description):

        self.db.create_alert(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            severity=severity,
            category=category,
            description=description
        )