import gc
import sys
import module_handler


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
    config.init_settings()
    processing.init_history()

    debug.log("[Main] Session started!", text_color="cyan")
    my_interface = interface.Interface()
    while True and not my_interface.terminate_program:
        pass
    sys.exit()

    debug.log(f"[Main] Application terminated, {e}")
    # del my_interface
    sys.exit(11)


if __name__ == "__main__":
    # Starting program
    main()
