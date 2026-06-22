from PySide6.QtGui import QPixmap

class PixMapManager:

    def __init__(self, settings):
        self.settings = settings

    def get(self, name):

        theme = 'light' if self.settings.get('ui','theme') == 'dark' else 'dark'
        return QPixmap(
            f'assets/{theme}/{name}.svg'
        )
