import socket
from threading import Thread


def _get_current_ip():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]

    except Exception:
        return "127.0.0.1"

    finally:
        sock.close()


class IPMonitor:

    def __init__(self, settings=None, alert_callback=None, interval=5):
        self.settings = settings
        self.alert_callback = alert_callback
        self.interval = interval

        self.current_ip = None

        self._running = False
        self._thread = None

    def start(self):

        if self._thread and self._thread.is_alive():
            return

        self._running = True

        self._thread = Thread(
            target=self._monitor_loop,
            name="IPMonitorThread",
            daemon=True
        )

        self._thread.start()

    def stop(self):

        self._running = False

        if self._thread:
            self._thread.join(timeout=2)

    def _monitor_loop(self):

        while self._running:

            if self._is_paused():
                self._sleep()
                continue

            if not self._dhcp_monitor_enabled():
                self._sleep()
                continue

            ip_address = _get_current_ip()

            if ip_address == "127.0.0.1":
                self._sleep()
                continue

            if self.current_ip is None:
                self.current_ip = ip_address
                self._sleep()
                continue

            if ip_address != self.current_ip:

                if self.alert_callback:
                    self.alert_callback(
                        severity="Baja",
                        category="DHCP Change",
                        description=(
                            f"Cambio de IP detectado: "
                            f"Anterior={self.current_ip} → Nueva={ip_address}"
                        )
                    )

                self.current_ip = ip_address

            self._sleep()

    def _sleep(self):

        from time import sleep
        sleep(self.interval)

    def _is_paused(self):
        return self.settings.get("monitoring", "on_paused")

    def _dhcp_monitor_enabled(self):
        return self.settings.get("detectors", "ip_changes")