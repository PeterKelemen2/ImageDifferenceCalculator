import json
import os

theme_path = "user_theme.json"
default_user_theme = '''{
    "bg": "#97F3FF",
    "accent": "#FFF3A4",
    "text": "#000000"
}'''


class UserTheme:
    def __init__(self, bg=None, accent=None, text=None):
        self.bg = bg
        self.accent = accent
        self.text = text

    def to_dict(self):
        return self.__dict__


def save_theme(theme):
    try:
        # theme_dict = theme.to_dict()
        with open(theme_path, "w") as json_file:
            json.dump(theme, json_file, indent=4)
    except FileNotFoundError:
        print("Error.")


def load_theme():
    if os.path.exists(theme_path):
        try:
            with open(theme_path, "r") as json_file:
                user_theme = json.load(json_file)
            return user_theme
        except FileNotFoundError:
            print("Error.")
    else:
        with open(theme_path, "w") as json_file:
            json_file.write(default_user_theme)
        with open(theme_path, "r") as json_file:
            user_theme = json.load(json_file)
        return user_theme
