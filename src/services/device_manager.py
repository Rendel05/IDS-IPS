from datetime import datetime, timedelta

from database.device import Device


class DeviceManager:
    def __init__(self, timeout: int = 300):
        self._devices: dict[str, Device] = {}
        self._timeout = timedelta(seconds=timeout)

    def observe(self, ip: str, mac: str | None = None) -> Device:

        now = datetime.now()

        device = self._devices.get(ip)

        if device is None:
            device = Device(
                ip=ip,
                mac=mac,
                first_seen=now,
                last_seen=now,
                packet_count=1
            )

            self._devices[ip] = device

        else:
            device.last_seen = now
            device.packet_count += 1

            if mac and not device.mac:
                device.mac = mac

        return device

    def get(self, ip: str) -> Device | None:
        return self._devices.get(ip)

    def get_devices(self) -> list[Device]:
        return list(self._devices.values())

    def remove_expired(self) -> list[Device]:

        now = datetime.now()
        removed = []

        for ip, device in list(self._devices.items()):
            if now - device.last_seen > self._timeout:
                removed.append(device)
                del self._devices[ip]

        return removed

    def clear(self):
        self._devices.clear()