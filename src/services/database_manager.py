from datetime import datetime, timedelta
import sqlite3
from threading import Lock
from pathlib import Path
from math import ceil



class DatabaseManager:
    def __init__(self):
        db_path = Path(__file__).parent.parent / "database/alerts.db"

        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.lock = Lock()
        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):
        with self.lock:
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
        with self.lock:
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

    def get_alerts(self, page: int, limit: int = 10, search: str = "", date_filter: int = 0, severity_filter: int = 0):
        page = max(1, int(page))
        limit = max(1, int(limit))

        conditions = []
        params = []

        if search:
            conditions.append("(category LIKE ? OR description LIKE ?)")
            params.extend([f"%{search}%", f"%{search}%"])

        date_map = {
            1: "datetime('now', '-24 hours')",
            2: "datetime('now', '-48 hours')",
            3: "datetime('now', '-7 days')",
        }
        if date_filter in date_map:
            conditions.append(f"timestamp >= {date_map[date_filter]}")

        severity_map = {
            1: "Baja",
            2: "Media",
            3: "Alta",
            4: "Crítica",
        }
        if severity_filter in severity_map:
            conditions.append("severity = ?")
            params.append(severity_map[severity_filter])

        where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        with self.lock:
            self.cursor.execute(f"""
                SELECT COUNT(*)
                FROM alerts
                {where_clause}
            """, params)

            total_records = self.cursor.fetchone()[0]
            total_pages = ceil(total_records / limit) if total_records else 1
            page = min(page, total_pages)
            offset = (page - 1) * limit

            self.cursor.execute(f"""
                SELECT *
                FROM alerts
                {where_clause}
                ORDER BY timestamp DESC
                LIMIT ?
                OFFSET ?
            """, params + [limit, offset])

            data = self.cursor.fetchall()

        return {
            "data": data,
            "total": total_records,
            "page": page,
            "pages": total_pages
        }

    def get_daily_alerts(self,limit:int = 10):
        with self.lock:
            self.cursor.execute("""
                SELECT *
                FROM alerts
                WHERE timestamp >= date('now','localtime')
                AND timestamp < datetime(date('now','localtime'),'+1 day')
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
        return self.cursor.fetchall()

    def get_alerts_per_hour(self):
        with self.lock:
            self.cursor.execute("""
                SELECT
                    CAST(strftime('%H', timestamp) AS INTEGER) AS hour,
                    COUNT(*) AS count
                FROM alerts
                WHERE DATE(timestamp) = DATE('now','localtime')
                GROUP BY hour
                ORDER BY hour
            """)

            rows = self.cursor.fetchall()

        result = {hour: 0 for hour in range(24)}
        for hour, count in rows:
            result[hour] = count

        return result


    def get_alert_summary(self) -> dict:

        today_str = datetime.now().strftime("%Y-%m-%d")
        yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


        query = """
        SELECT 
            COUNT(CASE WHEN DATE(timestamp) = ? THEN 1 END) AS today_total,
            COUNT(CASE WHEN DATE(timestamp) = ? AND severity IN ('Alta', 'Crítica') THEN 1 END) AS today_high_critical,
            COUNT(CASE WHEN DATE(timestamp) = ? THEN 1 END) AS yesterday_total,
            COUNT(CASE WHEN DATE(timestamp) = ? AND severity IN ('Alta', 'Crítica') THEN 1 END) AS yesterday_high_critical
        FROM alerts
        WHERE DATE(timestamp) IN (?, ?)
        """

        with self.lock:
            self.cursor.execute(
                query,
                (today_str, today_str, yesterday_str, yesterday_str, today_str, yesterday_str)
            )
            row = self.cursor.fetchone()

        if row:
            return {
                "today_total": row[0],
                "today_high_critical": row[1],
                "yesterday_total": row[2],
                "yesterday_high_critical": row[3]
            }

        return {
            "today_total": 0,
            "today_high_critical": 0,
            "yesterday_total": 0,
            "yesterday_high_critical": 0
        }


    def get_chart_values(self):
        with self.lock:
            self.cursor.execute("""
                SELECT 
                COUNT(CASE WHEN severity = 'Crítica' THEN 1 END) as critico,
                COUNT(CASE WHEN severity = 'Alta' THEN 1 END) as alta,
                COUNT(CASE WHEN severity = 'Media' THEN 1 END) as media,
                COUNT(CASE WHEN severity = 'Baja' THEN 1 END) as baja
                FROM alerts
                WHERE timestamp >= date('now','localtime')
                AND timestamp < datetime(date('now','localtime'),'+1 day')
            """)
        critical, high, medium, low = self.cursor.fetchone()
        return critical, high, medium, low

    def get_alert_details(self, alert_id):
        with self.lock:
            self.cursor.execute("""
            SELECT * 
            FROM alerts 
            WHERE id = ?
            """,
            (alert_id,)
            )
        return self.cursor.fetchone()


    def empty_alerts(self):
        with (self.lock):
            self.cursor.executescript("""
            DELETE FROM alerts;
            DELETE FROM sqlite_sequence
            WHERE name = 'alerts';
            """)
            self.connection.commit()

    def close(self):
        with self.lock:
            self.connection.close()
