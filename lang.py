import debug

# lang = "English"
lang_en = "assets/lang_en"
lang_hu = "assets/lang_hu"

lang_dict = dict()


def set_up_dict(lang_file):
    with open(lang_file, 'r', encoding="utf-8") as lang:
        for line in lang:
            entry = line.rstrip().split("=")
            lang_dict[entry[0]] = entry[1]
        return lang_dict


def load_lang(lang):
    if lang == "hungarian":
        debug.log(f"Loaded {lang} language to dictionary", text_color="cyan")
        return set_up_dict(lang_hu)
    elif lang == "english":
        debug.log(f"Loaded {lang} language to dictionary", text_color="cyan")
        return set_up_dict(lang_en)
    else:
        debug.log("Not supported language")


def print_button_list(button_list):
    print(button_list)
