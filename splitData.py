import os
import random
import argparse
import shutil
from tqdm import tqdm
from glob import glob

"""
Description:
  データセットをtrainとevalに分割する関数
Parameters:
  src_dir: 入力データセットディレクトリパス
  dst_dir: 出力データセットディレクトリパス
  seed: 乱数のシード
  ratio: train用/eval用データの分割比率(train : eval = ratio : 100 - ratio)
  ext: ファイル拡張子
"""
def splitData(
    src_dir='./resized_dataset',
    dst_dir='./cache',
    ext='jpg',
    train_val_ratio=0.9,
    seed=None,
    clean_dst=False
):
  ## 乱数設定
  if seed:
    print('split data randomly')
    random.seed(seed)

  ## train用とeval用に画像ファイルを分割する
  train_dir = os.path.join(dst_dir, 'train')
  eval_dir = os.path.join(dst_dir, 'val')
  print('Splitting {} -> {}, {}...'.format(src_dir, train_dir, eval_dir))

  ## 入力ディレクトリが存在しない場合強制終了
  assert os.path.isdir(os.path.join(src_dir, 'Annotations')), 'Not found Annotations at {}'.format(src_dir)
  assert os.path.isdir(os.path.join(src_dir, ext+'Images')), 'Not found Images at {}'.format(src_dir)

  ## 出力ディレクトリの用意
  if clean_dst:
    if os.path.isdir(train_dir):
      shutil.rmtree(train_dir)
    if os.path.isdir(eval_dir):
      shutil.rmtree(eval_dir)

  os.makedirs(os.path.join(train_dir, "Annotations"), exist_ok=True)
  os.makedirs(os.path.join(train_dir, ext+"Images"), exist_ok=True)

  os.makedirs(os.path.join(eval_dir, "Annotations"), exist_ok=True)
  os.makedirs(os.path.join(eval_dir, ext+"Images"), exist_ok=True)

  ## データ分割開始
  xml_files = glob(os.path.join(src_dir, "Annotations/*.xml"))
  random.shuffle(xml_files)

  def move_to(set_name, xml_paths):
    for xml_path in tqdm(xml_paths):
      file_name = os.path.splitext(os.path.basename(xml_path))[0]
      jpeg_path = os.path.join(src_dir, ext+"Images", "{}.{}".format(file_name, ext.lower()))
      dst_xml_path = os.path.join(dst_dir, set_name, "Annotations", "{}.xml".format(file_name))
      dst_img_path = os.path.join(dst_dir, set_name, ext+"Images", "{}.{}".format(file_name, ext.lower()))
      if os.path.isfile(jpeg_path):
        shutil.copyfile(xml_path, dst_xml_path)
        shutil.copyfile(jpeg_path, dst_img_path)
      else:
        print('skip', jpeg_path)

  train_num = int(len(xml_files) * train_val_ratio)
  move_to("train", xml_files[:train_num])
  move_to("val", xml_files[train_num:])

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--input", type=str, default='./resized_dataset')
  parser.add_argument("--output", type=str, default='./cache')
  parser.add_argument("--ext", type=str, default='jpg')
  parser.add_argument("--ratio", type=int, default=90)
  parser.add_argument("--seed", type=int, default=None)
  args = parser.parse_args()

  splitData(args.input, args.output, args.ext, args.ratio / 100., args.seed)
