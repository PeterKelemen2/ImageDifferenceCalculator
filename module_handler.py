import subprocess
import sys
import time

import debug

modules = ["opencv-python", "pillow"]


def check_if_modules_installed(installed_modules):
    missing_modules = [module
                       for module in modules
                       if module not in installed_modules]
    if missing_modules:
        debug.log(f"Module(s) {missing_modules} could not be installed, please install manually")
        sys.exit(f"Module(s) {missing_modules} could not be installed, please install manually")


def upgrade_pip():
    """
    Upgrade pip if necessary.
    """
    try:
        result = subprocess.run(["py", "-m", "pip", "install", "--upgrade", "pip", "--quiet"],
                                capture_output=True,
                                text=True)
        if 'Requirement already up-to-date' in result.stdout:
            debug.log("pip is already up-to-date.")
        else:
            debug.log("pip upgraded successfully.")
    except subprocess.CalledProcessError as e:
        debug.log(f"Error upgrading pip: {e.stderr}")
        sys.exit("Error upgrading pip.")


def module_handler():
    start_time = time.time()

    # # Upgrade pip to ensure it's up-to-date
    # debug.log("Upgrading pip if necessary...")
    # subprocess.run(["py", "-m", "pip", "install", "--upgrade", "pip", "--quiet"], check=True, shell=True)

    # Get installed modules
    result = subprocess.run(["py", "-m", "pip", "list"],
                            capture_output=True,
                            text=True)
    installed_modules = {line.split()[0]
                         for line in result.stdout.strip().split('\n')[2:]}

    # Install missing modules
    missing_modules = [module for module in modules if module not in installed_modules]
    if missing_modules:
        subprocess.run(["py", "-m", "pip", "install", *missing_modules, "--quiet"],
                       check=True,
                       shell=True)

    check_if_modules_installed(installed_modules)
    debug.log("All modules installed!")

    debug.log("Executed in {:.2f}s".format(time.time() - start_time))
