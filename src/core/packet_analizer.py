from scapy.layers.inet import IP, ICMP

class PacketAnalyzer:

    @staticmethod
    def analyze(packet):
        data = {}

        if IP in packet:
            data["src_ip"] = packet[IP].src
            data["dst_ip"] = packet[IP].dst
            data["protocol"] = packet[IP].proto

        if ICMP in packet:
            data["icmp_type"] = packet[ICMP].type

        return data