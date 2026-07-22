from dataclasses import dataclass, field
from datetime import datetime
import csv
import scapy.all as scapy
from scapy.error import Scapy_Exception
import ipaddress

from services.path_resolver import resource_path


@dataclass
class Device:
    ip: str
    mac: str | None = None
    hostname: str | None = None
    vendor: str | None = None
    is_gateway: bool = False
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)
    packet_count: int = 0


def _load_oui_database():
    oui_db = {}
    try:
        with open(resource_path("src/database/oui.csv"), encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                oui_db[row["Assignment"]] = row["Organization Name"]
    except FileNotFoundError:

        print("File not found")
    return oui_db


def _is_random_mac(mac: str) -> bool:
    try:
        first_byte = int(mac.split(":")[0], 16)
        return bool(first_byte & 0b00000010)
    except (ValueError, IndexError):
        return False


class NetworkScanner:

    def __init__(self):
        self.devices: dict[str, Device] = {}
        self.oui_map = _load_oui_database()

    def scan(self, timeout=2) -> dict:
        network = self._get_network_range()
        if not network:
            return self.get_snapshot()

        try:
            gateway_ip = scapy.conf.route.route("0.0.0.0")[2]
        except Exception:
            gateway_ip = None

        try:
            answered, _ = scapy.arping(
                network,
                timeout=timeout,
                verbose=False
            )
        except (Scapy_Exception, OSError):
            return self.get_snapshot()

        for _, received in answered:
            ip = received.psrc
            mac = received.hwsrc
            is_gateway = (ip == gateway_ip) if gateway_ip else False

            self._update_device(ip, mac, is_gateway)

        return self.get_snapshot()

    def get_snapshot(self) -> dict:

        snapshot = {}
        for mac, device in self.devices.items():
            snapshot[mac] = {
                "ip": device.ip,
                "hostname": device.hostname,
                "vendor": device.vendor,
                'is_gateway': device.is_gateway,
                "first_seen": device.first_seen,
                "last_seen": device.last_seen,
                "packet_count": device.packet_count,
            }
        return snapshot

    def _get_network_range(self) -> str | None:
        try:
            interface = scapy.conf.route.route("0.0.0.0")[0]
            local_ip = scapy.get_if_addr(interface)
            best_match = None

            for network, mask, _, route_interface, _, _ in scapy.conf.route.routes:
                if route_interface != interface:
                    continue
                if network == 0 or mask == 0:
                    continue

                network_addr = ipaddress.IPv4Address(network)
                netmask = ipaddress.IPv4Address(mask)

                candidate = ipaddress.IPv4Network(
                    f"{network_addr}/{netmask}",
                    strict=False
                )

                if candidate.prefixlen == 32:
                    continue
                if ipaddress.IPv4Address(local_ip) not in candidate:
                    continue

                if best_match is None or candidate.prefixlen > best_match.prefixlen:
                    best_match = candidate

            return str(best_match) if best_match else None
        except Exception:
            return None

    def _update_device(self, ip: str, mac: str, gateway: bool):
        now = datetime.now()
        device = self.devices.get(mac)

        if device is None:
            device = Device(
                ip=ip,
                mac=mac,
                vendor=self._resolve_vendor(mac),
                is_gateway=gateway
            )
            self.devices[mac] = device
        else:
            device.ip = ip
            device.last_seen = now
            device.packet_count += 1
            device.is_gateway = gateway

    def _resolve_vendor(self, mac: str) -> str:
        prefix = mac.replace(":", "").replace("-", "")[:6].upper()
        vendor = self.oui_map.get(prefix)

        if vendor:
            return vendor
        if _is_random_mac(mac):
            return "Random MAC (LAA)"
        return "Unknown vendor"