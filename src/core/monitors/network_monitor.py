from threading import Thread
from dataclasses import dataclass, field
from datetime import datetime
import csv

import scapy.all as scapy

@dataclass
class Device:
    ip: str
    mac: str | None = None

    hostname: str | None = None
    vendor: str | None = None

    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)

    packet_count: int = 0


def _load_oui_database():
    oui_db = {}

    with open("database/oui.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            oui_db[row["Assignment"]] = row["Organization Name"]

    return oui_db


class NetworkDeviceMonitor:

    def __init__(self, settings=None, interval=30):
        self.settings = settings
        self.interval = interval

        self.devices: dict[str, Device] = {}

        self.oui_map = _load_oui_database()

        self._running = False
        self._thread = None

    def start(self):

        if self._thread and self._thread.is_alive():
            return

        self._running = True

        self._thread = Thread(
            target=self._monitor_loop,
            name="NetworkDeviceMonitorThread",
            daemon=True
        )

        self._thread.start()

    def stop(self):

        self._running = False

        if self._thread:
            self._thread.join(timeout=2)

    def get_snapshot(self):

        snapshot = {}

        for mac, device in self.devices.items():

            snapshot[mac] = {
                "ip": device.ip,
                "hostname": device.hostname,
                "vendor": device.vendor,
                "first_seen": device.first_seen,
                "last_seen": device.last_seen,
                "packet_count": device.packet_count,
            }

        return snapshot

    def _monitor_loop(self):

        while self._running:

            self._arp_scan()

            self._sleep()

    def _arp_scan(self):

        pass

    def _update_device(self, ip: str, mac: str):

        now = datetime.now()

        if mac not in self.devices:

            self.devices[mac] = Device(
                ip=ip,
                mac=mac,
                vendor=self._resolve_vendor(mac),
            )

            return

        device = self.devices[mac]

        device.ip = ip
        device.last_seen = now
        device.packet_count += 1

    def _resolve_vendor(self, mac: str):

        prefix = mac.replace(":", "").replace("-", "")[:6].upper()

        info = self.oui_map.get(prefix)

        if info:
            print(info["name"])
        else:
            print("Fabricante desconocido")


    def _sleep(self):

        from time import sleep
        sleep(self.interval)

