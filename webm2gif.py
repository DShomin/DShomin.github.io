from glob import glob
from moviepy.editor import VideoFileClip

# TARGETDIR = "./assets/images/tmux/"
TARGETDIR = "/Users/ihomin/Documents/temp/"

file_list = glob(TARGETDIR + "*webm")

for file_name in file_list:
    new_name = file_name.replace("webm", "gif")
    crip = VideoFileClip(file_name)
    crip = crip.set_fps(10)
    crip.write_gif(new_name)
