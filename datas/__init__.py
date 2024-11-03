import pickle
import os


def load_metadata(path: str):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data


__sm_path = './datas/sign-metadata.pkl'
__vd_dir = './datas/sign-videos'
__metadata = load_metadata(__sm_path)


def get_video_by_label(label: str):
    vname = __metadata.get(label)
    if vname is None:
        return None
    vpath = os.path.join(__vd_dir, vname)
    return vpath
