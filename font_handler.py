import os
import shutil

import debug


def install_font(font_filename):
    try:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the font file
        font_path = os.path.join(script_dir, "assets", "fonts", font_filename)

        # Get the path to the system's font directory
        font_dir = os.path.join(os.getenv("SystemRoot"), "Fonts")

        # Copy the font file to the system's font directory
        shutil.copy(font_path, font_dir)

        debug.log("Font installed successfully.", text_color="cyan")
    except Exception as e:
        debug.log(f"Error installing font: {e}", text_color="red")
