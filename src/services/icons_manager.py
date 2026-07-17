from PySide6.QtGui import QIcon

from services.path_resolver import resource_path

class IconManager:


    def __init__(self, settings):
        self.settings = settings

    def get(self, name):
        theme = 'light' if self.settings.get('ui', 'theme') == 'dark' else 'dark'
        return QIcon(resource_path(f'src/assets/{theme}/{name}.svg'))
