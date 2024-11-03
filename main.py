import time
from models import generate_keywords
from datas import get_video_by_label
from utils.video import append_info, generate_video


start = time.time()

# text_id = 'Kualitas gambar medis yang baik sangat krusial untuk diagnosis yang akurat. Namun, seringkali gambar medis 2D terkendala oleh noise, artefak, atau resolusi rendah. Hal ini dapat menghambat kemampuan dokter dalam mendiagnosis penyakit dengan tepat.'
text_id = 'kami akan pergi ke sekolah'
keywords = generate_keywords(text_id)
print(keywords)
vpaths = [get_video_by_label(kw) for kw in keywords]
vpaths = [vp for vp in vpaths if vp is not None]
genp, t = generate_video(vpaths)
print(genp)
append_info(t, genp, text_id)

end = time.time()

print(end - start)

# print(len(sign_metadata.keys()))
