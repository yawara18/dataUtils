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
            if folderpath.startswith("GN"):
                ratio = 90
            splitData(folderpath, out, ext, ratio / 100.) #no random seed

src = '../dataset-20220420'
resized = 'resized'
dst = '../cache'
resize_batch(src, resized, 640, 360, 'PNG')
split_batch(resized, dst, 60, 'PNG')
