import os.path
import platform
import subprocess
import sys

import debug

windows_vlc_path = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"
windows_vlc_path_x86 = "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"
linux_vlc_path = "/usr/bin/vlc"

current_os = platform.system()
tries: int = 0


def vlc_windows_installer():
    global tries
    tries += 1
    debug.log(f"Windows version: {platform.version()}", text_color="cyan")
    # Checking if VLC path exists
    if os.path.exists(windows_vlc_path):
        debug.log("VLC installed!", text_color="cyan")
    else:
        debug.log("VLC not installed, installing...", text_color="yellow")
        # Download VLC installer
        subprocess.run(["curl", "-LO", "https://get.videolan.org/vlc/3.0.16/win64/vlc-3.0.16-win64.exe"])
        # Run the installer
        subprocess.run(["vlc-3.0.16-win64.exe", "/S", "/NORESTART"])

        # Checking if install was successful
        if os.path.exists(windows_vlc_path):
            debug.log("VLC installed successfully!", text_color="blue")
        else:
            # If unsuccessful, try again (only 3 times)
            if tries < 3:
                vlc_installer()
            else:
                debug.log("Could not install VLC, install manually to default location, exiting...", text_color="red")
                sys.exit("Could not install VLC, install manually to default location, exiting...")


def vlc_linux_installer():
    debug.log(f"Linux version: {platform.platform()}")

    if subprocess.run(["vlc", "--version"]):
        debug.log(f"VLC installed! - {subprocess.run(["vlc", "--version"])}")
    else:
        # Run installer command
        debug.log("VLC not installed, installing...")
        subprocess.run(["sudo", "apt", "install", "vlc"])


def vlc_installer():
    if current_os == "Windows":
        vlc_windows_installer()
    elif current_os == "Linux":
        vlc_linux_installer()
    else:
        debug.log("OS not supported!", text_color="red")
        sys.exit("OS not supported")


def open_video(file_path: str):
    debug.log("Opening video in VLC...", text_color="blue")
    if current_os == "Windows":
        file_path = file_path.replace("/", "\\")
        subprocess.Popen([windows_vlc_path, "--loop", file_path])

    elif current_os == "Linux":
        subprocess.run([linux_vlc_path, "--loop", file_path])
