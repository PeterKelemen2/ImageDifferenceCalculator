import sys
import module_handler


# Handling dependencies before program starts
# module_handler.module_handler()
# vlc_handler.vlc_installer()
# font_handler.install_font("Ubuntu-Regular.ttf")
# font_handler.install_font("Ubuntu-Bold.ttf")
# config.init_settings()
# processing.init_history()


# pyinstaller --onefile --add-data "assets;assets" main.py

def main():
    print("Starting...")
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

    try:
        debug.log("Session started!", text_color="cyan")
        my_interface = interface.Interface()
    except Exception as e:
        debug.log(f"Application terminated, {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Starting program
    main()
