import subprocess

modules = ["numpy", "opencv-python", "pillow", "python-vlc"]


def module_handler():
    for module in modules:
        subprocess.run(["pip", "install", module])
