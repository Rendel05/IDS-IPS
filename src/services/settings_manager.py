import json
from pathlib import Path

class SettingsManager:

    SETTINGS_FILE = Path(__file__).parent.parent / 'database/settings.json'

    def __init__(self):
        self.settings = self.load()

    def load(self):
        with open(self.SETTINGS_FILE,'r',encoding='utf-8') as file:
            return json.load(file)

    def save(self):
        with open(self.SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def get(self, *keys):
        value = self.settings

        for key in keys:
            value = value[key]

        return value

    def set(self, value, *keys):
        data = self.settings

        for key in keys[:-1]:
            data = data[key]

        data[keys[-1]] = value
        self.save()

