import importlib.util
import subprocess

modules = ["numpy", "opencv-python", "pillow", "python-vlc"]


def install_module(module: str):
    subprocess.run(["py", "-m", "pip", "install", module], shell=True)


def module_handler():
    subprocess.run(["py", "-m", "pip", "install", "--upgrade", "pip"], shell=True)
    for module in modules:
        if importlib.util.find_spec(module) is None:
            install_module(module)

        # try:
        #     import module
        # except ImportError:
        #     subprocess.run(["py", "-m", "pip", "install", module], shell=True)
