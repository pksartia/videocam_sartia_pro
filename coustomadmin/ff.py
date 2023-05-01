import subprocess

input_file = "public/chuha.mp4"
output_file = "output23.mp4"
text = "हेलो वर्ल्ड"
font_file = "TiroDevanagariHindi-Regular.ttf"
font_size = 72
font_color = "white"

# Construct the ffmpeg command
ffmpeg_cmd = ["ffmpeg", "-i", input_file, "-vf",
              f"drawtext=fontfile={font_file}:text='{text}':fontcolor={font_color}:fontsize={font_size}:x=(w-text_w)/2:y=(h-text_h)/2",
              "-codec:a", "copy", output_file]

# Run the ffmpeg command
subprocess.run(ffmpeg_cmd)
