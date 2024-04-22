import gc
import sys

import debug
import module_handler
import threading

# pyinstaller --onefile --add-data "assets;assets" main.py

my_interface = None


def initialize():
    module_handler.module_handler()

    import vlc_handler
    import font_handler
    import config
    import processing
    import debug

    vlc_handler.vlc_installer()
    font_handler.install_font("Ubuntu-Regular.ttf")
    font_handler.install_font("Ubuntu-Bold.ttf")
    font_handler.install_font("JetBrainsMono-Regular.ttf")
    config.init_settings()
    processing.init_history()

    debug.log("[Main] Session started!", text_color="cyan")


def get_interface():
    return my_interface


def main():
    initialize()

    import interface
    global my_interface
    my_interface = interface.Interface()
    debug.log("[Main] Interface initialized!", text_color="cyan")


if __name__ == "__main__":
    main()
