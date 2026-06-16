from .theme import TOKENS

STYLE_FILES = [
    "ui/styles/app.qss",
    'ui/styles/buttons.qss',
]


def load_stylesheet():
    qss = ""

    for path in STYLE_FILES:
        with open(path, encoding="utf-8") as file:
            qss += file.read() + "\n"

    for key, value in TOKENS.items():
        qss = qss.replace(f"${key}", value)

    return qss