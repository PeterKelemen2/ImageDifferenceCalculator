import os
import debug

config_path = "settings.config"


def init_settings():
    """
    Initializes settings by creating a configuration file with default values if it doesn't exist.

    This function checks if the configuration file specified by `config_path` exists. If not,
    it creates the file and writes default settings to it (language as 'english' and theme as 'palenight').

    Global Variables:
        config_path (str): Path to the configuration file.
    """
    global config_path
    if not os.path.exists(config_path):
        try:
            with open(config_path, "w") as f:
                debug.log("[Config] Created config file")
                f.write("lang=english\ntheme=palenight\nlog=On")
                debug.log("[Config] Default settings written to config file")
        except Exception as e:
            debug.log(str(e), text_color="red")


def save_settings(settings: list):
    """
    Saves settings to the configuration file.
    This function writes the provided settings to the configuration file specified by `config_path`.

    Parameters:
        settings (list): A list containing language and theme settings.
    """
    with open(config_path, 'w', encoding="utf-8") as file:
        file.write("lang=" + settings[0] + "\n")
        file.write("theme=" + settings[1] + "\n")
        file.write("log=" + settings[2] + "\n")
    debug.log("[Config] Saved settings to " + config_path, text_color="cyan")


def load_settings():
    """
    Loads settings from the configuration file.
    This function reads settings from the configuration file specified by `config_path`,
    extracts language and theme settings, and returns them as a list.

    Returns:
        list: A list containing language and theme settings.
    """
    global config_path
    lines = list()
    with open(config_path, 'r', encoding="utf-8") as file:
        for line in file:
            lines.append(line.rstrip().split("=")[1])
    debug.log(f"[Config] Loaded settings from {config_path}", text_color="cyan")
    return lines
