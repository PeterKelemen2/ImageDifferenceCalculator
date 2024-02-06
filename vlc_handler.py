import platform
import subprocess

import debug


def vlc_installer():
    match platform.system():
        case "Windows":
            debug.log(f"Windows version: {platform.version()}")
            if "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe" or "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe":
                debug.log("VLC installed!")
            else:
                debug.log("VLC not installed, installing...")
                # Download VLC installer
                subprocess.run(["curl", "-LO", "https://get.videolan.org/vlc/3.0.16/win64/vlc-3.0.16-win64.exe"])
                # Run the installer
                subprocess.run(["vlc-3.0.16-win64.exe"])

        case "Linux":
            debug.log(f"Linux version: {platform.platform()}")
            if subprocess.run(["vlc", "--version"]):
                debug.log(f"VLC installed! - {subprocess.run(["vlc", "--version"])}")
            else:
                # Run installer command
                debug.log("VLC not installed, installing...")
                subprocess.run(["sudo", "apt", "install", "vlc"])
