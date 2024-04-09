import gc
import sys
import module_handler
import test_interface


# pyinstaller --onefile --add-data "assets;assets" main.py

def main():
    module_handler.module_handler()

    import vlc_handler
    import font_handler
    import config
    import processing
    import debug
    import interface

    vlc_handler.vlc_installer()
    font_handler.install_font("Ubuntu-Regular.ttf")
    font_handler.install_font("Ubuntu-Bold.ttf")
    font_handler.install_font("JetBrainsMono-Regular.ttf")
    config.init_settings()
    processing.init_history()

    debug.log("[Main] Session started!", text_color="cyan")
    # my_interface = test_interface.Interface()
    my_interface = interface.Interface()


if __name__ == "__main__":
    # Starting program
    main()
