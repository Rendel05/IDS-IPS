from scapy.all import sniff

class PacketCapture:
    def __init__(self, callback):
        self.callback = callback

    def start(self):
        sniff(
            prn=self.callback,
            store=False
        )