import time
from models import generate_keywords
from datas import get_video_by_label
from utils.video import append_info, generate_video


def my_generator(prompt: str):
    keywords = []
    idx = 0
    yield None, 'Menerjemahkan...',  0
    for result, i in generate_keywords(prompt):
        idx = i
        if result is None:
            yield None, 'Menerjemahkan...',  i
        else:
            keywords = result
    yield None, 'Membuat video...', idx+1
    vpaths = [get_video_by_label(kw) for kw in keywords]
    vpaths = [vp for vp in vpaths if vp is not None]
    if len(vpaths) <= 0:
        yield None, 'Membuat video...', idx+2
    else:
        genp, t = generate_video(vpaths)
        append_info(t, genp, prompt)
        yield genp, 'Membuat video...', idx+2
