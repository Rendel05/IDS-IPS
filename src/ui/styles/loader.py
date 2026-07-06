import re

from .dark_theme import TOKENS as DARK_TOKENS
from .light_theme import TOKENS as LIGHT_TOKENS

STYLE_FILES = [
    "ui/styles/app.qss",
    "ui/styles/buttons.qss",
    "ui/styles/alerts.qss",
]

THEMES = {
    "dark": DARK_TOKENS,
    "light": LIGHT_TOKENS
}


def load_stylesheet(theme="dark"):
    qss = ""

    for path in STYLE_FILES:
        with open(path, encoding="utf-8") as file:
            qss += file.read() + "\n"

    tokens = THEMES.get(theme, DARK_TOKENS)

    pattern = re.compile(r"\$([A-Z0-9_]+)")
    qss = pattern.sub(lambda m: tokens.get(m.group(1), m.group(0)), qss)

    return qss