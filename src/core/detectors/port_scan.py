from collections import defaultdict, deque
from ipaddress import ip_address

from services.toast_manager import show_toast


IP_IGNORE_LIST = ['8.8.8.8']

class ScanDetector:

    def __init__(
        self,
        settings=None,
        alert_callback=None,
        updater=None,
        port_threshold=15,
        window_seconds=10,
        alert_cooldown=900
    ):
        self.settings = settings
        self.alert_callback = alert_callback
        self.updater = updater

        self.port_threshold = port_threshold
        self.window_seconds = window_seconds
        self.alert_cooldown = alert_cooldown

        self.traffic_history = defaultdict(deque)

        self.last_alert = {}

    def process(self, packet_info):

        if self._is_paused():
            return

        if not self._scanning_enabled():
            return

        destination_ip = packet_info.get("dst_ip")
        source_ip = packet_info.get("src_ip")
        destination_port = packet_info.get("dst_port")

        if not destination_ip or not source_ip or destination_port is None:
            return

        if source_ip in IP_IGNORE_LIST:
            return


        flow = (source_ip, destination_ip)

        current_time = packet_info["timestamp"]

        history = self.traffic_history[flow]
        history.append((current_time, destination_port))

        while history and history[0][0] < current_time - self.window_seconds:
            history.popleft()

        unique_ports = {port for _, port in history}

        if len(unique_ports) < self.port_threshold:
            return

        last_detection = self.last_alert.get(flow)

        if (
            last_detection and
            current_time - last_detection < self.alert_cooldown
        ):
            return

        self.last_alert[flow] = current_time

        if self.alert_callback:

            print(
                '[PORT SCAN] |'
                f"{destination_ip} | "
                f"ports={len(unique_ports)} "
                f"window={self.window_seconds}s"
            )


            self.alert_callback(
                severity="Crítica",
                category="Port Scan",
                description=(
                    f"Posible escaneo vertical detectado: {len(unique_ports)} puertos distintos "
                    f"hacia este dispositivo ({destination_ip}) "
                    f"en una ventana de {self.window_seconds}s "
                    f"desde {source_ip}"
                )
            )
            self.updater.scan_emit()
            show_toast('Escaneo de puertos',f"Posible escaneo detectado desde {source_ip}")

    def _is_paused(self):
        return self.settings.get(
            "monitoring",
            "on_paused"
        )

    def _scanning_enabled(self):
        return self.settings.get(
            "detectors",
            "nmap_scan"
        )