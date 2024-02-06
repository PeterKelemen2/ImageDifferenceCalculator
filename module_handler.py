import subprocess

modules = ["numpy", "opencv-python", "pillow", "python-vlc"]


def module_handler():
    for module in modules:
        # command = ["pip", "install", module]
        command = f"py -m pip install {module}"
        subprocess.run(command, shell=True)
