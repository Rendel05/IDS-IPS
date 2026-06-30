from collections import defaultdict


class ICMPFloodDetector:

    def __init__(self, settings=None, alert_callback=None):
        self.settings = settings
        self.alert_callback = alert_callback

        self.icmp_counter = defaultdict(list)
        self.active_alerts = set()

    def process(self, packet_info):

        if packet_info.get("icmp_type") != 8:
            return

        if self._is_paused():
            return

        if not self._icmp_flood_enabled():
            return

        src_ip = packet_info["src_ip"]
        current_time = packet_info["timestamp"]

        self.icmp_counter[src_ip].append(current_time)

        self.icmp_counter[src_ip] = [
            ts
            for ts in self.icmp_counter[src_ip]
            if current_time - ts < 10
        ]

        if len(self.icmp_counter[src_ip]) > 3: #Valores de prueba

            if src_ip in self.active_alerts:
                return

            self.active_alerts.add(src_ip)

            if self.alert_callback:
                self.alert_callback(
                    severity="Alta",
                    category="ICMP Flood",
                    description=f"Inundación ICMP detectada desde {src_ip}"
                )

    def _is_paused(self):
        return self.settings.get('monitoring','on_paused')

    def _icmp_flood_enabled(self):
        return self.settings.get('detectors','icmp_flood')

