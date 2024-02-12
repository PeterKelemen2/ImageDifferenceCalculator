import debug

config_path = "/settings.config"


def save_settings(settings):
    with open(config_path, 'w', encoding="utf-8") as file:
        file.write("lang=" + settings[0] + "\n")
        file.write("theme=" + settings[1] + "\n")


def load_settings():
    with open(config_path, 'r', encoding="utf-8") as file:
        pass
