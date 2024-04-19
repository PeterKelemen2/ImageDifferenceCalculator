import json


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
        with open("user_theme.json", "w") as json_file:
            json.dump(theme, json_file, indent=4)
    except FileNotFoundError:
        print("Error.")


def load_theme():
    try:
        with open("user_theme.json", "r") as json_file:
            global user_theme
            user_theme = json.load(json_file)
        print(user_theme)
        return user_theme
    except FileNotFoundError:
        print("Error.")
