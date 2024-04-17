import subprocess
import sys
import time

import debug
import main

modules = ["opencv-python", "pillow", "matplotlib", "numpy"]


def check_if_modules_installed(installed_modules):
    mi_modules = [module
                  for module in modules
                  if module not in installed_modules]
    if len(mi_modules) > 0:
        debug.log(f"[Modules] Module(s) {mi_modules} could not be installed, please install manually",
                  text_color="red",
                  timestamp_color="red")
        sys.exit(f"[Modules] Module(s) {mi_modules} could not be installed, please install manually")


def upgrade_pip():
    """
    Upgrade pip if necessary.
    """
    try:
        result = subprocess.run(["py", "-m", "pip", "install", "--upgrade", "pip", "--quiet"],
                                capture_output=True,
                                text=True)
        if 'Requirement already up-to-date' in result.stdout:
            debug.log("[Modules] pip is already up-to-date.")
        else:
            debug.log("[Modules] pip upgraded successfully.")
    except subprocess.CalledProcessError as e:
        debug.log(f"[Modules] Error upgrading pip: {e.stderr}")
        sys.exit("[Modules] Error upgrading pip.")


def module_handler():
    start_time = time.time()
    global modules

    # # Upgrade pip to ensure it's up-to-date
    # debug.log("Upgrading pip if necessary...")
    # subprocess.run(["py", "-m", "pip", "install", "--upgrade", "pip", "--quiet"], check=True, shell=True)

    # Get installed modules
    result = subprocess.run(["py", "-m", "pip", "list"],
                            capture_output=True,
                            text=True)
    installed_modules = {line.split()[0]
                         for line in result.stdout.strip().split('\n')[2:]}

    # Installing missing modules
    missing_modules = [module for module in modules if module not in installed_modules]
    if missing_modules:
        subprocess.run(["py", "-m", "pip", "install", *missing_modules, "--quiet"],
                       check=True,
                       shell=True)

    check_if_modules_installed(installed_modules)

    debug.log("[Modules] All modules installed!", text_color="cyan")

    debug.log("[Modules] Executed in {:.2f}s".format(time.time() - start_time), text_color="cyan")
