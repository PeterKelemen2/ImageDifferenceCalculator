import debug

lang = "English"
lang_en = "assets/lang_en"
lang_hu = "assets/lang_hu"

lang_dict = dict()


def load_lang(lang="English"):
    if lang == "English":
        debug.log(f"Program language: {lang}", text_color="cyan")
        with open(lang_en, 'r') as lang_file:
            for line in lang_file:
                print(line)
    else:
        debug.log("Not supported language")
