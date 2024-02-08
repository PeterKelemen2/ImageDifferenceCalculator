import importlib.util
import subprocess

import debug

modules = ["numpy", "opencv-python", "pillow"]


def module_handler():
    """
    Function to handle the installation of required Python modules.

    This function checks if required modules are installed, and if not, installs them.

    Args:
        None

    Returns:
        None
    """
    # Upgrade pip to ensure it's up-to-date
    debug.log("Updating pip...")
    subprocess.run(["py", "-m", "pip", "install", "--upgrade", "pip", "--quiet"], shell=True)
    debug.log("Pip updated or newest version already installed!")

    # Check for modules that need to be installed
    debug.log("Checking for missing modules...")
    modules_to_install = [module for module in modules if importlib.util.find_spec(module) is None]

    debug.log("Modules to install: " + str(modules_to_install))

    # Install missing modules, if any
    if modules_to_install:
        debug.log("Installing missing modules...")
        subprocess.run(["py", "-m", "pip", "install", *modules_to_install], shell=True)
        debug.log("Missing modules installed!")

    debug.log("All modules installed!")
