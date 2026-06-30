from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Device:
    ip: str
    mac: str | None = None

    hostname: str | None = None
    vendor: str | None = None

    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)

    packet_count: int = 0