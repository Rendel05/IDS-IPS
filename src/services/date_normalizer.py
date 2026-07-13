from datetime import datetime

DAYS = [
    "Lunes", "Martes", "Miércoles", "Jueves",
    "Viernes", "Sábado", "Domingo"
]

MONTHS = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]


def normalize_timestamp(timestamp: str) -> str:
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
    return f"{DAYS[dt.weekday()]} {dt.day} de {MONTHS[dt.month - 1]} de {dt.year} a las {dt.strftime('%H:%M:%S')}"

def normalize_datetime(dt: datetime) -> str:
    return (
        f"{DAYS[dt.weekday()]} {dt.day} de "
        f"{MONTHS[dt.month - 1]} de {dt.year} "
        f"a las {dt.strftime('%H:%M:%S')}"
    )