import os
import subprocess

from vidstab import VidStab

import debug

video_suffix = "_stabilized.mp4"


def stabilize_video(input_file):
    debug.log(f"Started stabilizing {input_file}...")
    first_pass_output = input_file[:-4] + "_first_pass.mp4"
    debug.log(f"First pass output file: {first_pass_output}")
    first_pass = VidStab(kp_method='FAST', threshold=30)
    first_pass.stabilize(input_path=input_file,
                         output_path=first_pass_output,
                         border_size="auto")
    convert_to_cfr(first_pass_output)

    debug.log(f"Second pass input: {first_pass_output[:-4] + "_cbr_converted.mp4"}")
    debug.log(f"Second pass output: {first_pass_output[:-4] + "_second_pass.mp4"}")
    second_pass = VidStab(kp_method='FAST')
    second_pass.stabilize(input_path=first_pass_output[:-4] + "_cbr_converted.mp4",
                          output_path=first_pass_output[:-4] + "_second_pass.mp4",
                          border_size="auto")
    convert_to_cfr(first_pass_output[:-4] + "_second_pass.mp4")


def convert_to_cfr(input_file):
    if os.path.exists(input_file[:-4] + "_cbr_converted.mp4"):
        # os.remove(input_file[:-4] + "_cbr_converted.mp4")
        pass
    command = [
        'C:/ffmpeg/bin/ffmpeg',
        '-i', input_file,
        '-r', "95",  # Set the target frame rate
        '-c:v', 'libx264',  # Video codec
        '-crf', '25',  # Constant Rate Factor (quality)
        '-preset', 'slower',  # Encoding preset for speed
        '-c:a', 'aac',  # Audio codec
        '-b:a', '128k',  # Audio bitrate
        '-movflags', '+faststart',  # Fast start for web playback
        str(input_file[:-4] + "_cbr_converted.mp4")  # Output file
    ]
    debug.log(
        f"Started converting stabilized video to CFR format... {input_file}", text_color="cyan")
    subprocess.run(command)
    os.remove(input_file)
    debug.log("Finished converting stabilized video!", text_color="cyan")
