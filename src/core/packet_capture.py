from scapy.all import sniff
from scapy.layers.inet import IP, ICMP


class PacketCapture:

    def __init__(self, callback):
        self.callback = callback

    def start(self):
        sniff(
            filter="icmp",
            prn=self.process_packet,
            store=False
        )

    def process_packet(self, packet):

        if IP not in packet or ICMP not in packet:
            return

        if packet[ICMP].type != 8:
            return

        packet_info = {
            "src_ip": packet[IP].src,
            "dst_ip": packet[IP].dst,
            "icmp_type": packet[ICMP].type
        }

        self.callback(packet_info)