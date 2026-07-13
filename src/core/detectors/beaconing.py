from collections import defaultdict, deque
from ipaddress import ip_address
from statistics import mean, median, pstdev

from services.toast_manager import show_toast

class BeaconDetector:


    _EXCLUDED_PROTOCOL = {17,}
    _EXCLUDED_PORT = { 53, 123}

    _MIN_CYCLES_FOR_WINDOW = 5

    def __init__(
        self,
        settings=None,
        alert_callback=None,
        updater=None,
        packet_threshold=30,
        max_deviation=0.5,
        alert_cooldown=900,
        max_cv=0.10,
        min_observation_window=300,
        include_dst_port_in_key=False,
        max_size_cv=0.20,
        max_avg_packet_size=1000,
        min_suspicious_count=3,
        inactive_flow_ttl=86400,
        cleanup_interval=300,
    ):
        self.settings = settings
        self.alert_callback = alert_callback
        self.updater = updater

        self.packet_threshold = packet_threshold
        self.max_deviation = max_deviation
        self.alert_cooldown = alert_cooldown

        self.max_cv = max_cv
        self.min_observation_window = min_observation_window
        self.include_dst_port_in_key = include_dst_port_in_key
        self.max_size_cv = max_size_cv
        self.max_avg_packet_size = max_avg_packet_size
        self.min_suspicious_count = min_suspicious_count
        self.inactive_flow_ttl = inactive_flow_ttl
        self.cleanup_interval = cleanup_interval

        self.suspicious_counts = defaultdict(int)


        self.traffic_history = defaultdict(
            lambda: deque(maxlen=self.packet_threshold)
        )

        self.last_alert = {}
        self._last_cleanup = 0

    def process(self, packet_info):

        if self._is_paused():
            return

        if not self._beaconing_enabled():
            return

        destination_ip = packet_info.get("dst_ip")
        source_ip = packet_info.get("src_ip")

        if not destination_ip or not source_ip:
            return

        current_time = packet_info.get("timestamp")

        if current_time is None:
            return

        self._cleanup_inactive_flows(current_time)

        if (
                ip_address(destination_ip).is_private or
                ip_address(destination_ip).is_multicast or
                ip_address(destination_ip).is_loopback or
                ip_address(destination_ip).is_link_local or
                ip_address(destination_ip).is_unspecified
        ):
            return


        if packet_info.get('dst_port') in self._EXCLUDED_PORT:
            return

        flow = self._build_flow_key(packet_info, source_ip, destination_ip)
        packet_size = packet_info.get("length", 0)

        history = self.traffic_history[flow]
        history.append((current_time, packet_size))

        if len(history) < self.packet_threshold:
            return

        timestamps = [entry[0] for entry in history]
        sizes = [entry[1] for entry in history]

        observation_window = timestamps[-1] - timestamps[0]


        deltas = [
            timestamps[i] - timestamps[i - 1]
            for i in range(1, len(timestamps))
        ]

        average_interval = mean(deltas)
        median_interval = median(deltas)

        if average_interval <= 0 or median_interval <= 0:
            return

        required_window = max(
            180,
            median_interval * 5
        )

        if observation_window < required_window:
            return

        standard_deviation = pstdev(deltas)
        cv_mean = standard_deviation / average_interval

        mad = median([abs(delta - median_interval) for delta in deltas])
        cv_median = mad / median_interval

        interval_is_regular = (
            cv_mean <= self.max_cv and cv_median <= self.max_cv
        )

        average_size = mean(sizes)
        size_is_regular = True
        looks_like_bulk_transfer = False

        if average_size > 0:
            size_deviation = pstdev(sizes)
            size_cv = size_deviation / average_size
            size_is_regular = size_cv <= self.max_size_cv

        is_periodic_candidate = (
            interval_is_regular
            and size_is_regular
            and not looks_like_bulk_transfer
        )

        if not is_periodic_candidate:
            self.suspicious_counts[flow] = 0
            return

        self.suspicious_counts[flow] += 1

        if self.suspicious_counts[flow] < self.min_suspicious_count:
            return

        last_detection = self.last_alert.get(flow)

        if (
            last_detection is not None
            and current_time - last_detection < self.alert_cooldown
        ):
            return

        self.last_alert[flow] = current_time

        if self.alert_callback:
            self.alert_callback(
                severity="Alta",
                category="Beaconing",
                description=(
                    f"Patrón de beaconing con un intervalo promedio de "
                    f"{average_interval:.2f}s detectado hacia {destination_ip} "
                )
            )
            if self.updater:
                self.updater.beacon_emit()
            show_toast('Beacon', f"Patrón de beaconing detectado hacia {destination_ip}")

    def _build_flow_key(self, packet_info, source_ip, destination_ip):
        if self.include_dst_port_in_key:
            return (
                source_ip,
                destination_ip,
                packet_info.get("dst_port"),
                packet_info["protocol"],
            )

        return source_ip, destination_ip, packet_info["protocol"]

    def _cleanup_inactive_flows(self, current_time):
        if current_time - self._last_cleanup < self.cleanup_interval:
            return

        self._last_cleanup = current_time

        inactive_flows = [
            flow for flow, history in self.traffic_history.items()
            if history and current_time - history[-1][0] > self.inactive_flow_ttl
        ]

        for flow in inactive_flows:
            self.traffic_history.pop(flow, None)
            self.last_alert.pop(flow, None)
            self.suspicious_counts.pop(flow, None)

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