import module_handler
import vlc_handler

# Handling dependencies before program starts
module_handler.module_handler()
vlc_handler.vlc_installer()

import debug
import interface


def main():
    debug.log("Session started!")
    my_interface = interface.Interface()


if __name__ == "__main__":
    # Starting program
    main()
