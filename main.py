import module_handler
import debug
import interface
import vlc_handler


def main():
    debug.log("Session started!")

    # Has issues
    module_handler.module_handler()
    vlc_handler.vlc_installer()
    my_interface = interface.Interface()


if __name__ == "__main__":
    module_handler.module_handler()
    main()
