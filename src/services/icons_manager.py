from PySide6.QtGui import QIcon

class IconManager:

    def __init__(self, settings):
        self.settings = settings

    def get(self, name):

        theme = 'light' if self.settings.get('ui','theme') == 'dark' else 'dark'

        return QIcon(
            f"assets/{theme}/{name}.svg"
        )
