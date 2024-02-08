import importlib.util
import subprocess

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
    subprocess.run(["py", "-m", "pip", "install", "--upgrade", "pip", "--quiet"], shell=True)

    # Check for modules that need to be installed
    modules_to_install = [module for module in modules if importlib.util.find_spec(module) is None]

    # Install missing modules, if any
    if modules_to_install:
        subprocess.run(["py", "-m", "pip", "install", *modules_to_install], shell=True)
