from threading import Thread, Event
import psutil

from services.toast_manager import show_toast

WHITELIST = {
    "node.exe",
    "python.exe",
    "code.exe",
    "docker.exe",
}


def _get_open_ports():

    ports = {}

    for connection in psutil.net_connections(kind="inet"):

        if connection.status != psutil.CONN_LISTEN:
            continue

        try:
            process = psutil.Process(connection.pid)
            ports[connection.laddr.port] = process.name()

        except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                TypeError
        ):
            ports[connection.laddr.port] = "Unknown"

    return ports


class PortMonitor:

    def __init__(self, settings=None, alert_callback=None,updater = None,interval=10):
        self.settings = settings
        self.alert_callback = alert_callback
        self.interval = interval
        self.updater = updater


        self.known_ports = _get_open_ports()

        self._running = False
        self._thread = None
        self._stop_event = Event()

    def start(self):

        if self._thread and self._thread.is_alive():
            return

        self._running = True
        self._stop_event.clear()

        self._thread = Thread(
            target=self._monitor_loop,
            name="PortMonitorThread",
            daemon=True
        )

        self._thread.start()

    def stop(self):

        self._running = False
        self._stop_event.set()

        if self._thread:
            self._thread.join(timeout=2)

    def _monitor_loop(self):

        while self._running:

            if self._is_paused():
                self._wait()
                continue

            if not self._port_monitor_enabled():
                self._wait()
                continue

            current_ports = _get_open_ports()

            for port in sorted(current_ports.keys() - self.known_ports.keys()):

                process_name = current_ports[port]

                if process_name in WHITELIST:
                    continue


                if self.alert_callback:
                    self.alert_callback(
                        severity="Alta",
                        category="New Port Open",
                        description=f"Nuevo puerto local abierto detectado: {port} ({process_name})"
                    )
                self.updater.port_emit()
                show_toast('Puerto Local',f"Nuevo puerto local abierto detectado: {port} ({process_name})")


            self.known_ports = current_ports
            self._wait()

    def _wait(self):
        self._stop_event.wait(self.interval)

    def _is_paused(self):
        return self.settings.get("monitoring", "on_paused")

    def _port_monitor_enabled(self):
        return self.settings.get("detectors", "new_port")

