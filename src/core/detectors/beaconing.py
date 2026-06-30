from collections import defaultdict, deque
from ipaddress import ip_address
from statistics import mean, pstdev

#Lista de IP comunes, si alguien retoma esto en el futuro que encuentre una forma más elegante de solucionar esto, Pedro M.

IP_IGNORE_LIST = [
    "192.178.220.188",
    "172.64.148.235",
    "172.64.155.209",
    "142.251.186.188",
    "173.194.208.188",
    "192.178.56.170",
    "151.101.2.137",
    "104.18.39.21",
    "224.0.1.187",
    "108.156.224.11",
    '192.178.52.170',
    '142.251.186.188',
    '192.178.220.188',
    '104.18.37.228',
    '35.190.80.1',
    '224.0.0.252',
    '192.178.56.74',
    '172.64.150.28',
    '192.178.56.74',
    '172.64.148.235',
    '192.178.52.138',
    '192.178.56.202',
    '142.250.189.10',
    '34.100.128.0',
    '224.0.0.1',
    '224.0.0.251',
    '142.250.189.10',
    '34.54.194.141',
    '142.251.152.119',
    '142.251.116.188',
    '34.36.57.103',
    '185.199.109.133',
    '34.160.81.0',
    '192.178.57.10',
    '142.250.114.188',
    '162.159.134.234',
    '142.251.45.42',
    '104.18.32.47',
    '104.18.32.47',
    '162.159.138.232',
    '104.18.32.47',
    '142.251.46.10',
    '142.250.177.10',
    '172.67.160.146',
    '104.21.44.219',
    '23.227.38.33',
    '23.227.39.20',
    '142.251.219.202',
    '192.178.57.42',
    '142.250.65.202',
    '192.178.52.202',
    '192.178.56.234',
    '142.250.115.188',
    '104.26.6.219',
    '192.178.56.42',
    '192.178.52.234 '
]

class BeaconDetector:

    def __init__(
        self,
        settings=None,
        alert_callback=None,
        packet_threshold=8,
        max_deviation=0.5,
        alert_cooldown=900
    ):
        self.settings = settings
        self.alert_callback = alert_callback

        self.packet_threshold = packet_threshold
        self.max_deviation = max_deviation
        self.alert_cooldown = alert_cooldown

        self.traffic_history = defaultdict(
            lambda: deque(maxlen=self.packet_threshold)
        )

        self.last_alert = {}

    def process(self, packet_info):

        if self._is_paused():
            return

        if not self._beaconing_enabled():
            return

        destination_ip = packet_info.get("dst_ip")
        source_ip = packet_info.get("src_ip")

        if not destination_ip or not source_ip:
            return

        try:
            if ip_address(destination_ip).is_private:
                return
        except ValueError:
            return

        if destination_ip in IP_IGNORE_LIST:
            return


        flow = (
            packet_info["src_ip"],
            packet_info["dst_ip"],
            packet_info.get("dst_port"),
            packet_info["protocol"]
        )

        current_time = packet_info["timestamp"]

        history = self.traffic_history[flow]
        history.append(current_time)

        if len(history) < self.packet_threshold:
            return

        deltas = [
            history[i] - history[i - 1]
            for i in range(1, len(history))
        ]
        average_interval = mean(deltas)
        standard_deviation = pstdev(deltas)

        if average_interval <= 1:
            return

        if standard_deviation >= self.max_deviation:
            return

        last_detection = self.last_alert.get(flow)

        if (
            last_detection and
            current_time - last_detection < self.alert_cooldown
        ):
            return

        self.last_alert[flow] = current_time

        if self.alert_callback:
            #testing
            print(
                f"{destination_ip} | "
                f"avg={average_interval:.2f} "
                f"std={standard_deviation:.3f} "
                f"count={len(history)}"
            )

            self.alert_callback(
                severity="Crítica",
                category="Beaconing",
                description=(
                    f"Patrón de beaconing con un intervalo promedio de {average_interval:.2f}s detectado hacia {destination_ip} "
                )
            )

    def _is_paused(self):
        return self.settings.get(
            "monitoring",
            "on_paused"
        )

    def _beaconing_enabled(self):
        return self.settings.get(
            "detectors",
            "beaconing"
        )

