from .dark_theme import TOKENS as DARK_TOKENS
from .light_theme import TOKENS as LIGHT_TOKENS

STYLE_FILES = [
    "ui/styles/app.qss",
    'ui/styles/buttons.qss',
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

    for key, value in tokens.items():
        qss = qss.replace(f"${key}", value)

    return qss