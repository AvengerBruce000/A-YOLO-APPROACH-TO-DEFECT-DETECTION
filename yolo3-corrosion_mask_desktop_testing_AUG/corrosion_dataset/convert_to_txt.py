import argparse
import json
import os
import sys

import numpy as np
from PIL import Image
import os.path as osp
import warnings
 
 
from labelme import utils
import base64


def idd_class_to_number(cls):
    #class_mapping = {'crs': '0'}
    class_mapping = {'corrosion': '0'}
    if cls in class_mapping.keys():
        return class_mapping[cls]
    else:
        return None
    
    
    
    
    
####################################################
def get_obj_index(image):
    n = np.max(image)
    print(n)
    return n

def draw_mask( num_obj, mask, image):
    for index in range(num_obj):
        for i in range(np.shape(mask)[1]):
            for j in range(np.shape(mask)[0]):
                at_pixel = image.getpixel((i, j))
                if at_pixel == index + 1:
                    mask[j, i, index] =1
    return mask
####################################################






def convert_json(annotation_folder, image_folder):
    
    mask_dir = "./mask/"
    
    
    
    cls_chck = idd_class_to_number

    print(image_folder)
    #out = open('D:/trash/4560/small_corrosion/json/annotation.txt', 'w')
    out = open('../annotation.txt', 'w')
    skipped = 0
    img_type = '.jpg'
    

    for root, subdirs, files in os.walk(annotation_folder):
        print(root)
        for file in files:
            if ".json" not in file:
                continue
            with open(os.path.join(root, file)) as f:
                jf = json.load(f)
            objects = jf['shapes']
            polygons_line = ''
            for object in objects:
                c = cls_chck(object['label'])
                if c is None:
                    continue
                polygon = object['points']
                min_x = sys.maxsize
                max_x = 0
                min_y = sys.maxsize
                max_y = 0
                polygon_line = ''
                for x, y in polygon:
                    if x > max_x: max_x = x
                    if y > max_y: max_y = y
                    if x < min_x: min_x = x
                    if y < min_y: min_y = y
                    polygon_line += ',{},{}'.format(x, y)
                if max_x - min_x <= 1.0 or max_y - min_y <= 1.0:
                    skipped += 1
                    continue
                #polygons_line += ' {},{},{},{},{}'.format(int(min_x), int(min_y), int(max_x), int(max_y), c) + polygon_line
                polygons_line += ' {},{},{},{},{}'.format(int(min_x), int(min_y), int(max_x), int(max_y), c)
            #if polygons_line == '': continue
            ##########################################################################
            ##########################################################################
            file_name = file.split('.')[0]
            img_file = file_name + img_type
            ##########################################################################
            ##########################################################################
            annotation_line = os.path.join(image_folder, img_file) + polygons_line
            
            
            
            
            
            
            
            ################################################################
            mask_img = Image.open(mask_dir+file_name+'.png')
            num_obj = get_obj_index(mask_img)
            mask = np.zeros([np.shape(mask_img)[0], np.shape(mask_img)[1], num_obj], dtype=np.uint8)
            mask = draw_mask(num_obj, mask, mask_img)
            print("shape of mask : ", mask.shape)
            
            mask_line = ''
            first_flag = True
            
            c = 0
            for i in range(0, 26):
                for j in range(0, 26):
                    
                    
                    if mask.shape[2] != 0:
                        
                        temp = mask[i*16:i*16+15, j*16:j*16+15, 0]
                            
                        if sum(list(temp.reshape(-1)))>128:
                            if first_flag:
                                mask_line = mask_line + "+"+str(j*16)+","+str(i*16)+","+str(j*16+15)+","+str(i*16+15)+",0"
                            else:
                                mask_line = mask_line + " "+str(j*16)+","+str(i*16)+","+str(j*16+15)+","+str(i*16+15)+",0"
                            c = c+1
                            first_flag = False
            #if no big enough object to bedecteted 
            #use the max one
            if first_flag:
                #mask_line = mask_line + "+"+str(max_j*16)+","+str(max_i*16)+","+str(max_j*16+15)+","+str(max_i*16+15)+",0"         
                mask_line = mask_line + "+"    
            annotation_line = annotation_line + mask_line
            ################################################################
            
            
            
            
            
            
            
            print(img_file)
            print("num of blocks:", c)
            print(annotation_line, file=out)
    print('I have skipped total number of {} boxes due its width or height being <=1.0'.format(skipped))
    out.close()





def section_1():
    count = os.listdir("./corrosion/") 
    index = 0
    for i in range(0, len(count)):
        path = os.path.join("./corrosion", count[i])

        if os.path.isfile(path) and path.endswith('json'):
            data = json.load(open(path))
            
            
            ###########################################
            file_name = count[i].split('.')[0]
            ###########################################
            
            
            imageData = data.get("imageData")
            if not imageData:
                imagePath = os.path.join(os.path.dirname(path), data["imagePath"])
                with open(imagePath, "rb") as f:
                    imageData = f.read()
                    imageData = base64.b64encode(imageData).decode("utf-8")
            img = utils.img_b64_to_arr(imageData)
            
            label_name_to_value = {'_background_': 0}
            for shape in data['shapes']:
                label_name = shape['label']
                if label_name in label_name_to_value:
                    label_value = label_name_to_value[label_name]
                else:
                    label_value = len(label_name_to_value)
                    label_name_to_value[label_name] = label_value
            
            # label_values must be dense
            label_values, label_names = [], []
            for ln, lv in sorted(label_name_to_value.items(), key=lambda x: x[1]):
                label_values.append(lv)
                label_names.append(ln)
            
            assert label_values == list(range(len(label_values)))
            
            lbl, _  = utils.shapes_to_label(img.shape, data['shapes'], label_name_to_value)

            label_path = "./mask"
            if not os.path.exists(label_path):
                os.mkdir(label_path)
            utils.lblsave(osp.join(label_path, str(file_name)+'.png'), lbl)
            warnings.warn('info.yaml is being replaced by label_names.txt')
            index = index+1
            print('Saved : %s' % str(file_name))





if __name__ == '__main__':

    section_1()    


    #dataset_labels = "D:/trash/4560/small_corrosion/json/"
    dataset_labels = "./corrosion/"
    #dataset_images = "D:/trash/4560/small_corrosion/"
    dataset_images = "./corrosion_dataset/corrosion/"
    convert_json(dataset_labels, dataset_images)
