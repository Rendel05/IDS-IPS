from collections import defaultdict
from time import time


class DetectionEngine:

    def __init__(self):
        self.icmp_counter = defaultdict(list)
        self.active_alerts = set()

    def process(self, packet_info):

        src_ip = packet_info["src_ip"]

        current_time = time()

        self.icmp_counter[src_ip].append(current_time)

        self.icmp_counter[src_ip] = [
            ts
            for ts in self.icmp_counter[src_ip]
            if current_time - ts < 10
        ]

        if len(self.icmp_counter[src_ip]) > 9:

            if src_ip not in self.active_alerts:

                self.active_alerts.add(src_ip)

                print(
                    f"[ALERT] ICMP Flood {src_ip}"
                )