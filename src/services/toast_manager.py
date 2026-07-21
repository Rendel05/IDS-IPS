from win11toast import toast

from services.settings_manager import SettingsManager
from services.path_resolver import resource_path

ICON_PATH = resource_path('src/assets/node_toast.png')
APP_ID = 'IDS/IPS.app'


def show_toast(title: str, body: str):
    auth = SettingsManager().get('notifications', 'enabled')
    if not auth:
        return

    toast(
        title=title,
        body=body,
        icon=ICON_PATH,
        app_id=APP_ID
    )
