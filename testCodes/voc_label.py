import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

base_path = '/data/datasets/'

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(year, image_id):
    in_file = open('%sVOCdevkit/VOC%s/Annotations/%s.xml'%(base_path, year, image_id))
    out_file = open('%sVOCdevkit/VOC%s/labels/%s.txt'%(base_path,year, image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes: # or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

# wd = getcwd()
save_base_path = 'datasets'
for year, image_set in sets:
    if not os.path.exists('%sVOCdevkit/VOC%s/labels/'%(base_path,year)):
        os.makedirs('%sVOCdevkit/VOC%s/labels/'%(base_path,year))
    image_ids = open('%sVOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(base_path,year, image_set)).read().strip().split()
    list_file = open('%s/%s_%s.txt'%(save_base_path, year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('%sVOCdevkit/VOC%s/JPEGImages/%s.jpg\n'%(base_path, year, image_id))
        convert_annotation(year, image_id)
    list_file.close()

os.system("cat 2007_train.txt 2007_val.txt 2012_train.txt 2012_val.txt > train.txt")
os.system("cat 2007_train.txt 2007_val.txt 2007_test.txt 2012_train.txt 2012_val.txt > train.all.txt")