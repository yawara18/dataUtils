from resizeData import resizeImage
from splitData import splitData
import os 

def resize_batch(srcpath, out, w, h, ext):
    candidates = os.listdir(srcpath)
    for name in candidates:
        folderpath = os.path.join(srcpath, name)
        if os.path.isdir(folderpath):
            dstpath = os.path.join(out, name)
            resizeImage(folderpath, dstpath, w, h, ext)

def split_batch(srcpath, out, ratio, ext):
    candidates = os.listdir(srcpath)
    for name in candidates:
        folderpath = os.path.join(srcpath, name)
        if os.path.isdir(folderpath):
            splitData(folderpath, out, ext, ratio / 100.) #no random seed

resize_batch('../dataset-20220420', 'resized', 640, 360, 'PNG')
split_batch('../dataset-20220420', 'cache', 60, 'PNG')
