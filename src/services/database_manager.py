import sqlite3
from pathlib import Path

class DatabaseManager:

    def __init__(self):
        db_path = Path(__file__).parent.parent / "database/alerts.db"

        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                severity TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)

        self.connection.commit()

    def create_alert(
            self,
            timestamp: str,
            severity: str,
            category: str,
            description: str
    ):
        self.cursor.execute("""
            INSERT INTO alerts(
                timestamp,
                severity,
                category,
                description
            )
            VALUES (?, ?, ?, ?)
        """, (
            timestamp,
            severity,
            category,
            description
        ))

        self.connection.commit()

    def get_alerts(self):
        self.cursor.execute("""
            SELECT *
            FROM alerts
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    def delete_alert(self, alert_id: int):
        self.cursor.execute(
            "DELETE FROM alerts WHERE id = ?",
            (alert_id,)
        )

        self.connection.commit()

    def close(self):
        self.connection.close()