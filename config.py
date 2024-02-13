import debug

config_path = "settings.config"


def save_settings(settings):
    with open(config_path, 'w', encoding="utf-8") as file:
        file.write("lang=" + settings[0] + "\n")
        file.write("theme=" + settings[1] + "\n")
    debug.log("Saved settings to " + config_path, text_color="cyan")


def load_settings():
    global config_path
    lines = list()
    with open(config_path, 'r', encoding="utf-8") as file:
        for line in file:
            lines.append(line.rstrip().split("=")[1])
    debug.log(f"Loaded settings from {config_path}", text_color="cyan")
    return lines
