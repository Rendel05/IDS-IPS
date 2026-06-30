import time
from scapy.all import sniff
from scapy.layers.inet import IP, ICMP, TCP, UDP
from threading import Thread, Event

class PacketCapture:

    def __init__(self, callback, bpf_filter="ip"):
        self.callback = callback
        self.bpf_filter = bpf_filter
        self._stop_event = Event()
        self._thread = None

    def start(self):

        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()

        self._thread = Thread(
            target=self._capture_loop,
            daemon=True
        )

        self._thread.start()

    def stop(self):

        self._stop_event.set()

        if self._thread:
            self._thread.join(timeout=2)

    def _capture_loop(self):

        while not self._stop_event.is_set():
            sniff(
                filter=self.bpf_filter,
                prn=self.process_packet,
                store=False,
                timeout=1
            )

    def process_packet(self, packet):

        if IP not in packet:
            return

        packet_info = {
            "timestamp": time.time(),
            "src_ip": packet[IP].src,
            "dst_ip": packet[IP].dst,
            "protocol": packet[IP].proto,
            "length": len(packet)
        }

        if TCP in packet:
            packet_info["src_port"] = packet[TCP].sport
            packet_info["dst_port"] = packet[TCP].dport
            packet_info["flags"] = packet[TCP].flags

        if UDP in packet:
            packet_info["src_port"] = packet[UDP].sport
            packet_info["dst_port"] = packet[UDP].dport

        if ICMP in packet:
            packet_info["icmp_type"] = packet[ICMP].type

        self.callback(packet_info)
