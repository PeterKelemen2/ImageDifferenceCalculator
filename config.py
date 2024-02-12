import debug

config_path = "settings.config"


def save_settings(settings):
    with open(config_path, 'w', encoding="utf-8") as file:
        file.write("lang=" + settings[0] + "\n")
        file.write("theme=" + settings[1] + "\n")


def load_settings():
    lines = list()
    with open(config_path, 'r', encoding="utf-8") as file:
        for line in file:
            lines.append(line.rstrip().split("=")[1])
    return lines
