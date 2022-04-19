import os
import glob
import xml.etree.ElementTree as ET
import xmltodict
import json
import argparse
from xml.dom import minidom
from collections import OrderedDict

def loadMapJson(path):
    with open(path, "r") as f:
        label_map_dict = json.load(f)
    attrDict = dict()
    attrDict["categories"] = []
    for key in label_map_dict:
        attrDict["categories"].append({
            "supercategory": "none",
            "id": label_map_dict[key],
            "name": key
        })
    return attrDict

def XML2JSON(xmlFiles, outputPath, mapPath):
    attrDict = loadMapJson(mapPath)
    images = list()
    annotations = list()
    image_id = 0
    for file in xmlFiles:
        image_id = image_id + 1
        annotation_path=file
        image = dict()
        doc = xmltodict.parse(open(annotation_path).read(), force_list=('object'))
        image['file_name'] = str(doc['annotation']['filename'])
        image['height'] = int(doc['annotation']['size']['height'])
        image['width'] = int(doc['annotation']['size']['width'])
        image['id'] = image_id
        print ("File Name: {} and image_id {}".format(file, image_id))
        images.append(image)
        id1 = 1
        if 'object' in doc['annotation']:
            if len(doc['annotation']['object']) == 0:
                print("File: {} doesn't have any object".format(file))
                continue
            for obj in doc['annotation']['object']:
                for value in attrDict["categories"]:
                    annotation = dict()
                    if str(obj['name']) == value["name"]:
                        annotation["iscrowd"] = 0
                        annotation["image_id"] = image_id
                        x1 = int(obj["bndbox"]["xmin"])  - 1
                        y1 = int(obj["bndbox"]["ymin"]) - 1
                        x2 = int(obj["bndbox"]["xmax"]) - x1
                        y2 = int(obj["bndbox"]["ymax"]) - y1
                        annotation["bbox"] = [x1, y1, x2, y2]
                        annotation["area"] = float(x2 * y2)
                        annotation["category_id"] = value["id"]
                        annotation["ignore"] = 0
                        annotation["id"] = id1
                        annotation["segmentation"] = [[x1,y1,x1,(y1 + y2), (x1 + x2), (y1 + y2), (x1 + x2), y1]]
                        id1 +=1
                        annotations.append(annotation)
        else:
            print("File: {} not found".format(file))

    attrDict["images"] = images
    attrDict["annotations"] = annotations
    attrDict["type"] = "instances"

    jsonString = json.dumps(attrDict)
    if os.path.exists(outputPath):
        os.remove(outputPath)
    with open(outputPath, "w") as f:
        f.write(jsonString)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="./Annotations")
    parser.add_argument("--output", type=str, default="./train.json")
    parser.add_argument("--label", type=str, default="./labelmap.json")
    args = parser.parse_args()
    trainXMLFiles=glob.glob(os.path.join(args.input, '*.xml'))
    XML2JSON(trainXMLFiles, args.output, args.label)
