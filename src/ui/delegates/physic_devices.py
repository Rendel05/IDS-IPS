from PySide6.QtWidgets import QLabel


class PhysicCard:
    def __init__(self, device_type:str, device_monitor,layout):
        self.device_type =  device_monitor.get_devices().get(device_type,[])
        self.layout = layout
        self.set()

    def set(self):

        for device in self.device_type:
            self.layout.addWidget(QLabel(f'{device['name']}({'activo' if device['enabled'] else 'desactivado'})'))
