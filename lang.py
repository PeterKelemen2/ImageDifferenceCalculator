import debug

# File paths for language dictionaries
lang_en = "assets/lang_en"
lang_hu = "assets/lang_hu"


def set_up_dict(lang_file):
    """
    Sets up a language dictionary from a language file.

    This function reads a language file and creates a dictionary mapping keys to their respective translations.

    Parameters:
        lang_file (str): The path to the language file.

    Returns:
        dict: A dictionary containing translations.
    """
    debug.log(f"Setting up language dictionary from {lang_file}")
    lang_dict = dict()
    with open(lang_file, 'r', encoding="utf-8") as lang:
        for line in lang:
            entry = line.rstrip().split("=")
            # debug.log(f"Entry: {entry}")
            if len(entry) == 2:
                lang_dict[entry[0]] = entry[1]
    return lang_dict


def load_lang(lang):
    """
    Loads language dictionary based on the specified language.

    This function loads a language dictionary based on the provided language string.
    It logs the loading process and returns the corresponding dictionary.

    Parameters:
        lang (str): The language to load ("hungarian" or "english").

    Returns:
        dict: A dictionary containing translations for the specified language.
            If the language is not supported, returns None.
    """
    if lang == "hungarian":
        debug.log(f"Loaded {lang} language to dictionary", text_color="cyan")
        return set_up_dict(lang_hu)
    elif lang == "english":
        debug.log(f"Loaded {lang} language to dictionary", text_color="cyan")
        return set_up_dict(lang_en)
    else:
        debug.log("Not supported language")
        return None
