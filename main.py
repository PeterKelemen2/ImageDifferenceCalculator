import module_handler
import vlc_handler
import font_handler
import config
import processing

# Handling dependencies before program starts
module_handler.module_handler()
vlc_handler.vlc_installer()
font_handler.install_font("Ubuntu-Regular.ttf")
font_handler.install_font("Ubuntu-Bold.ttf")
config.init_settings()
processing.init_history()

import debug
import interface


def main():
    debug.log("Session started!", text_color="cyan")
    my_interface = interface.Interface()


# pyinstaller --onefile --add-data "assets;assets" main.py

if __name__ == "__main__":
    # Starting program
    main()
