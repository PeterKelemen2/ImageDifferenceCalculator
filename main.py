import debug
import interface
import vlc_handler


def main():
    debug.log("Session started!")
    vlc_handler.vlc_installer()
    my_interface = interface.Interface()


if __name__ == "__main__":
    main()
