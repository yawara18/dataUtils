import os
import argparse
import xml.etree.ElementTree as et
import shutil
import cv2
from tqdm import tqdm
from glob import glob

"""
Description:
    画像をリサイズする関数
Parameters:
    src_dir: 入力データディレクトリパス
    dst_dir: リサイズ後の出力データディレクトリパス
    width: 画像サイズ幅
    height: 画像サイズ高さ
    ext: 画像拡張子
"""
def resizeImage(
    src_dir='full_dataset',
    dst_dir='resized_dataset',
    width=640,
    height=640,
    ext='jpg'
):
  print('Resizing {} -> {}...'.format(src_dir, dst_dir))

  ## 入力ディレクトリが存在しない場合強制終了
  assert os.path.isdir(os.path.join(src_dir, 'Annotations')), 'Not found Annotations at {}'.format(src_dir)
  assert os.path.isdir(os.path.join(src_dir, ext + 'Images')), 'Not found Images at {}'.format(src_dir)

  ## 出力ディレクトリの用意
  if os.path.exists(dst_dir):
      shutil.rmtree(dst_dir)
  xml_dst_dir = os.path.join(dst_dir, "Annotations")
  img_dst_dir = os.path.join(dst_dir, ext + "Images")
  os.makedirs(xml_dst_dir, exist_ok=True)
  os.makedirs(img_dst_dir, exist_ok=True)

  ## xmlファイルに対応する画像ファイルをリサイズ
  xml_files = glob(os.path.join(src_dir, "Annotations/*.xml"))
  xml_files = sorted(xml_files)
  for xml_file in tqdm(xml_files):
      xml = et.parse(xml_file)
      root = xml.getroot()

      ## 画像ファイルが存在しなければスキップ
      file_name = os.path.splitext(os.path.basename(xml_file))[0]
      jpeg_path = os.path.join(src_dir, ext + "Images", "{}.{}".format(file_name, ext))
      if not os.path.exists(jpeg_path):
          print('Not found image file: {} (xml_file: {})'.format(jpeg_path, xml_file))
          continue

      ## xml中のサイズデータを修正
      width_xml = root.find("size/width")
      width_org = int(width_xml.text)
      width_xml.text = str(width)
      height_xml = root.find("size/height")
      height_org = int(height_xml.text)
      height_xml.text = str(height)
      w_ratio = width / width_org
      h_ratio = height / height_org

      bndboxes = root.findall("object/bndbox")
      for bbox in bndboxes:
          xmin = bbox.find("xmin")
          ymin = bbox.find("ymin")
          xmax = bbox.find("xmax")
          ymax = bbox.find("ymax")
          xmin.text = str(round(float(xmin.text) * w_ratio))
          ymin.text = str(round(float(ymin.text) * h_ratio))
          xmax.text = str(round(float(xmax.text) * w_ratio))
          ymax.text = str(round(float(ymax.text) * h_ratio))

      ## 画像サイズを修正
      xml_dest_path = os.path.join(xml_dst_dir, "{}.xml".format(file_name))
      xml.write(xml_dest_path, "utf-8")
      
      img = cv2.imread(jpeg_path)
      img_resized = cv2.resize(img, (width, height))
      img_dest_path = os.path.join(img_dst_dir, "{}.{}".format(file_name, ext.lower()))
      cv2.imwrite(img_dest_path, img_resized)

      print('debug', xml_dest_path)
      print('debug', jpeg_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default='full_dataset')
    parser.add_argument("--output", type=str, default='resized_dataset')
    parser.add_argument("--ext", type=str, default='PNG')
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=640)
    args = parser.parse_args()

    resizeImage(args.input, args.output, args.width, args.height, args.ext)


