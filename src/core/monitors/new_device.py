import threading
import winreg
from datetime import datetime, timedelta
from time import sleep
from pathlib import Path
from services.toast_manager import show_toast


def _filetime_to_datetime(filetime: int) -> datetime | None:
    if not filetime:
        return None
    try:
        return datetime(1601, 1, 1) + timedelta(microseconds=filetime / 10)
    except (OverflowError, OSError):
        return None


def _clean_app_name(raw_name: str) -> str:
    raw_name = raw_name.replace("NonPackaged:", "").strip()
    if "#" in raw_name:
        return Path(raw_name.split("#")[-1]).stem
    return raw_name.split("#")[-1].split("_")[0] or raw_name


_REGISTRY_PATHS = {
    "cam": r"Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam",
    "mic": r"Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone",
}

_EMPTY_DEVICE_ENTRY = {
    "cam_access": "-", "cam_state": "-", "cam_last_used": "-",
    "mic_access": "-", "mic_state": "-", "mic_last_used": "-",
}

_DEVICE_CLASS_PATHS = {
    "cam": (
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Microsoft\Windows Media Foundation\HardwareMFT",  # fallback
    ),
}

_DEVICE_CLASS_GUIDS = {
    "cam": "{ca3e7ab9-b4c3-4ae6-8251-579ef933890f}",
    "mic": "{c166523c-fe0c-4a94-a586-f1a80cfbbf3e}",
}

_ENUM_ROOT = r"SYSTEM\CurrentControlSet\Enum"


def _read_device_names_by_class(class_guid: str) -> list[dict]:

    devices = []

    try:
        enum_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, _ENUM_ROOT)
    except OSError:
        return devices

    bus_index = 0
    while True:
        try:
            bus_name = winreg.EnumKey(enum_key, bus_index)
        except OSError:
            break
        bus_index += 1

        try:
            bus_key = winreg.OpenKey(enum_key, bus_name)
        except OSError:
            continue

        device_index = 0
        while True:
            try:
                device_id = winreg.EnumKey(bus_key, device_index)
            except OSError:
                break
            device_index += 1

            try:
                device_key = winreg.OpenKey(bus_key, device_id)
            except OSError:
                continue

            instance_index = 0
            while True:
                try:
                    instance_id = winreg.EnumKey(device_key, instance_index)
                except OSError:
                    break
                instance_index += 1

                try:
                    instance_key = winreg.OpenKey(device_key, instance_id)
                except OSError:
                    continue

                try:
                    guid, _ = winreg.QueryValueEx(instance_key, "ClassGUID")
                except FileNotFoundError:
                    winreg.CloseKey(instance_key)
                    continue

                if guid.lower() == class_guid.lower():
                    device_info = _extract_device_info(
                        instance_key, bus_name, device_id, instance_id
                    )
                    devices.append(device_info)

                winreg.CloseKey(instance_key)

            winreg.CloseKey(device_key)

        winreg.CloseKey(bus_key)

    winreg.CloseKey(enum_key)
    return devices


def _extract_device_info(
    key, bus: str, device_id: str, instance_id: str
) -> dict:
    def _get_val(name: str, default="Unknown"):
        try:
            val, _ = winreg.QueryValueEx(key, name)
            return val or default
        except FileNotFoundError:
            return default

    friendly_name = _get_val("FriendlyName")
    manufacturer = _get_val("Mfg", "Unknown manufacturer")
    device_desc = _get_val("DeviceDesc", friendly_name)
    hardware_id = _get_val("HardwareID", "")

    # HardwareID puede ser lista o string
    if isinstance(hardware_id, list):
        hardware_id = hardware_id[0] if hardware_id else ""

    if ";" in manufacturer:
        manufacturer = manufacturer.split(";")[-1].strip()

    try:
        config_flags, _ = winreg.QueryValueEx(key, "ConfigFlags")
        enabled = not bool(config_flags & 0x1)
    except FileNotFoundError:
        enabled = True

    return {
        "id": f"{bus}\\{device_id}\\{instance_id}",
        "name": friendly_name if friendly_name != "Unknown" else device_desc,
        "manufacturer": manufacturer,
        "hardware_id": hardware_id,
        "bus": bus,
        "enabled": enabled,
    }


class DeviceMonitor:

    def __init__(self, settings=None, alert_callback=None, updater = None,interval: int = 5):
        self.settings = settings
        self.alert_callback = alert_callback
        self.interval = interval
        self.updater = updater

        self._snapshot: dict = {}
        self._devices: dict[str, list[dict]] = {"cam": [], "mic": []}
        self._active_states: dict = {}
        self._lock = threading.Lock()

        self._running = False
        self._thread: threading.Thread | None = None

    def start(self):
        if self._thread and self._thread.is_alive():
            return

        snapshot = self._build_snapshot()
        devices = self._build_device_list()


        with self._lock:
            self._snapshot = snapshot
            self._devices = devices

        self._running = True
        self._thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True,
            name="DeviceMonitorThread",
        )
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=self.interval + 1)

    def get_snapshot(self) -> dict:
        with self._lock:
            return dict(self._snapshot)

    def get_devices(self) -> dict[str, list[dict]]:
        with self._lock:
            return {k: list(v) for k, v in self._devices.items()}

    def _monitor_loop(self):
        while self._running:
            self._sleep()

            if not self._device_monitor_enabled():
                continue

            snapshot = self._build_snapshot()
            devices = self._build_device_list()

            with self._lock:
                self._snapshot = snapshot
                self._devices = devices

            self._check_alerts(snapshot)


    def _build_device_list(self) -> dict[str, list[dict]]:
        return {
            "cam": _read_device_names_by_class(_DEVICE_CLASS_GUIDS["cam"]),
            "mic": _read_device_names_by_class(_DEVICE_CLASS_GUIDS["mic"]),
        }

    def _read_registry_entries(self, prefix: str) -> list[dict]:
        path = _REGISTRY_PATHS[prefix]
        entries = []

        try:
            root_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)
        except FileNotFoundError:
            return entries

        def parse_children(parent_key):
            index = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(parent_key, index)
                except OSError:
                    break
                index += 1
                try:
                    subkey = winreg.OpenKey(parent_key, subkey_name)
                except OSError:
                    continue
                entries.append(self._parse_registry_entry(subkey, subkey_name))
                winreg.CloseKey(subkey)

        index = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(root_key, index)
            except OSError:
                break
            index += 1
            try:
                subkey = winreg.OpenKey(root_key, subkey_name)
            except OSError:
                continue
            if subkey_name == "NonPackaged":
                parse_children(subkey)
            else:
                entries.append(self._parse_registry_entry(subkey, subkey_name))
            winreg.CloseKey(subkey)

        winreg.CloseKey(root_key)
        return entries

    def _parse_registry_entry(self, subkey, raw_name: str) -> dict:
        try:
            permission, _ = winreg.QueryValueEx(subkey, "Value")
            has_access = permission == "Allow"
        except FileNotFoundError:
            has_access = True

        try:
            last_start, _ = winreg.QueryValueEx(subkey, "LastUsedTimeStart")
        except FileNotFoundError:
            last_start = 0

        try:
            last_stop, _ = winreg.QueryValueEx(subkey, "LastUsedTimeStop")
        except FileNotFoundError:
            last_stop = 0

        return {
            "app_name": _clean_app_name(raw_name),
            "has_access": has_access,
            "currently_active": last_start != 0 and last_stop == 0,
            "last_start": last_start,
            "last_stop": last_stop,
        }

    def _build_snapshot(self) -> dict:
        snapshot = {}
        for prefix in ("cam", "mic"):
            for entry in self._read_registry_entries(prefix):
                app = entry["app_name"]
                if app not in snapshot:
                    snapshot[app] = dict(_EMPTY_DEVICE_ENTRY)
                access_txt, state_txt, last_used_txt = self._format_entry(entry)
                snapshot[app][f"{prefix}_access"] = access_txt
                snapshot[app][f"{prefix}_state"] = state_txt
                snapshot[app][f"{prefix}_last_used"] = last_used_txt
        return snapshot

    def _format_entry(self, entry: dict) -> tuple[str, str, str]:
        if not entry["has_access"]:
            return "No access", "Blocked", "—"
        if entry["currently_active"]:
            date = _filetime_to_datetime(entry["last_start"])
            since = date.strftime("%Y-%m-%d %H:%M:%S") if date else "In use"
            return "Access granted", "ACTIVE (in use)", f"Since {since}"
        date = _filetime_to_datetime(entry["last_stop"])
        last_used = date.strftime("%Y-%m-%d %H:%M:%S") if date else "No usage record"
        return "Access granted", "Inactive", last_used

    def _check_alerts(self, snapshot: dict):
        device_labels = {"cam": "cámara", "mic": "micrófono"}
        for app, info in snapshot.items():
            for prefix, label in device_labels.items():
                state = info[f"{prefix}_state"]
                key = f"{app}|{prefix}"
                is_active_now = "ACTIVE" in state
                was_active = self._active_states.get(key, False)
                self._active_states[key] = is_active_now
                turned_on = is_active_now and not was_active
                turned_off = was_active and not is_active_now
                if not (turned_on or turned_off):
                    continue

                if turned_off:
                    self.updater.device_off_emit()
                    continue

                if not self.alert_callback:
                    continue

                description = (
                    f"El {label} fue activado por '{app}'."
                    if label == "micrófono"
                    else f"La {label} fue activada por '{app}'."
                )
                toast_title = 'Nuevo Dispositivo'
                toast_msg = (
                    f'El {label} ha sido encendido'
                    if label == 'micrófono'
                    else f'La {label} ha sido encendida'
                )
                category = "New Device"

                self.alert_callback(
                    severity="Media",
                    category=category,
                    description=description,
                )
                self.updater.device_emit()
                show_toast(toast_title, toast_msg)


    def _sleep(self):
        sleep(self.interval)

    def _device_monitor_enabled(self) -> bool:
        return self.settings.get("detectors", "new_device")