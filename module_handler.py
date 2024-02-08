import importlib.util
import subprocess
import time

modules = ["numpy", "opencv-python", "pillow", "python-vlc"]


def install_module(module: str):
    subprocess.run(["py", "-m", "pip", "install", module], shell=True)


def module_handler():
    subprocess.run(["py", "-m", "pip", "install", "--upgrade", "pip", "--quiet"], shell=True)
    start_time = time.time()

    modules_to_install = [module for module in modules if importlib.util.find_spec(module) is None]
    if modules_to_install:
        subprocess.run(["py", "-m", "pip", "install", *modules_to_install], shell=True)

    end_time = time.time()
    elapsed_time = "{:.2f}".format(end_time - start_time)
    print(f"Elapsed time: {elapsed_time}s")
