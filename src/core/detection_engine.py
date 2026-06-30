class DetectionEngine:
    def __init__(self, detectors=None):
        self.detectors = detectors or []

    def process(self, packet_info):
        for detector in self.detectors:
            detector.process(packet_info)