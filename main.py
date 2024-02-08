import module_handler

# Call module_handler at the beginning of program
# module_handler.module_handler()

import debug
import interface
import vlc_handler


def main():
    debug.log("Session started!")

    my_interface = interface.Interface()


if __name__ == "__main__":
    # Handling dependencies before program starts
    module_handler.module_handler()
    vlc_handler.vlc_installer()

    # Starting program
    main()
