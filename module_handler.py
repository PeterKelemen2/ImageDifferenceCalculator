import importlib.util
import subprocess

modules = ["numpy", "opencv-python", "pillow"]


def install_module(module: str):
    subprocess.run(["py", "-m", "pip", "install", module], shell=True)


def module_handler():
    subprocess.run(["py", "-m", "pip", "install", "--upgrade", "pip", "--quiet"], shell=True)

    modules_to_install = [module for module in modules if importlib.util.find_spec(module) is None]
    if modules_to_install:
        subprocess.run(["py", "-m", "pip", "install", *modules_to_install], shell=True)
