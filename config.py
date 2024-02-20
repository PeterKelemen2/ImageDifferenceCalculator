import os

import debug

config_path = "settings.config"


def init_settings():
    global config_path
    if not os.path.exists(config_path):
        try:
            with open(config_path, "w") as f:
                print("Created")
                f.write("lang=english\ntheme=palenight")
        except Exception as e:
            debug.log(str(e), text_color="red")


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
