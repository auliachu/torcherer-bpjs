from moviepy.editor import VideoFileClip, concatenate_videoclips
from datetime import datetime
from math import floor
import os


def get_info():
    ct = datetime.now()
    ts = floor(ct.timestamp() * 1000)
    fn = str(ts) + '.mp4'
    return fn, str(ct)


def generate_video(paths: list[str]):
    fn, t = get_info()
    clips = [VideoFileClip(path) for path in paths]
    final_clip = concatenate_videoclips(clips, method='compose')
    dir = './results/generated'
    os.makedirs(dir, exist_ok=True)
    path = os.path.join(dir, fn)
    final_clip.write_videofile(path)
    return path, t


__history_path = './results/history.txt'


def append_info(t, fn, text):
    with open(__history_path, 'a+') as f:
        f.write(t + '\n')
        f.write(fn + '\n')
        f.write(text + '\n')
        f.write('\n')
