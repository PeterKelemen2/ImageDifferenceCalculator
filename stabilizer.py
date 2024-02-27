import os
import subprocess

from vidstab import VidStab

import debug

video_suffix = "_stabilized.mp4"


def stabilize_video(input_file):
    debug.log(f"Started stabilizing {input_file}...")
    stabilizer = VidStab()
    stabilizer.stabilize(input_path=input_file,
                         output_path=input_file[:-4] + video_suffix)
    convert_to_cfr(str(input_file[:-4] + video_suffix))


def convert_to_cfr(input_file):
    if os.path.exists(input_file[:-4] + "_cbr_converted.mp4"):
        os.remove(input_file[:-4] + "_cbr_converted.mp4")
    command = [
        'C:/ffmpeg/bin/ffmpeg',
        '-i', input_file,
        '-r', "95",  # Set the target frame rate
        '-c:v', 'libx264',  # Video codec
        '-crf', '15',  # Constant Rate Factor (quality)
        '-preset', 'slower',  # Encoding preset for speed
        '-c:a', 'aac',  # Audio codec
        '-b:a', '128k',  # Audio bitrate
        '-movflags', '+faststart',  # Fast start for web playback
        # str(input_file[:-4] + "_cbr_converted.mp4")  # Output file
        str(input_file[:-4] + "_cbr_converted.mp4")  # Output file
    ]
    debug.log(
        f"Started converting stabilized video to CFR format... {input_file}", text_color="cyan")
    subprocess.run(command)
    os.remove(input_file)
    debug.log("Finished converting stabilized video!", text_color="cyan")
