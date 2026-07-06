from PySide6.QtCore import Signal, QObject


class GlobalUpdater(QObject):
    icmp_signal = Signal(str)
    port_signal = Signal(str)
    ip_signal = Signal(str)
    scan_signal = Signal(str)
    beacon_signal = Signal(str)
    device_signal = Signal(str)


    def __init__(self):
        super().__init__()

    def icmp_emit(self):
        self.icmp_signal.emit('icmp')

    def port_emit(self):
        self.port_signal.emit('tcp')

    def ip_emit(self):
        self.ip_signal.emit('ipv4')

    def scan_emit(self):
        self.scan_signal.emit('tcp')

    def beacon_emit(self):
        self.beacon_signal.emit('beacon')

    def device_emit(self):
        self.device_signal.emit('device')







