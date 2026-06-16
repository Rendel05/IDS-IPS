from collections import defaultdict
from time import time

class DetectionEngine:

    def __init__(self):
        self.icmp_counter = defaultdict(list)

    def process(self, packet_data):
        if packet_data.get("icmp_type") is None:
            return None

        src = packet_data["src_ip"]

        now = time()

        self.icmp_counter[src].append(now)

        self.icmp_counter[src] = [
            ts
            for ts in self.icmp_counter[src]
            if now - ts < 10
        ]

        if len(self.icmp_counter[src]) > 100:
            return {
                "type": "ICMP Flood",
                "source": src
            }

        return None