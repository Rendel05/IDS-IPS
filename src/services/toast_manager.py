from win11toast import toast
from pathlib import Path

from services.settings_manager import SettingsManager

BASE_DIR = Path(__file__).resolve().parent.parent
icon_path = BASE_DIR / "assets" / "node_toast.png"


def show_toast(title:str,body:str):
    auth = SettingsManager().get('notifications', 'enabled')
    if not auth:
        return

    toast(
        title=title,
        body=body,
        icon=f'{icon_path}',
        app_id='IDS/IPS'
    )
