import argparse
import yolo_testing
import yolo_1
import yolo_2
import yolo_3
from PIL import Image
import keras

def main(path, model_index):
    # class YOLO defines the default value, so suppress any default here
    if model_index == 0:
        my_yolo = yolo_testing.YOLO()
    if model_index == 1:
        my_yolo = yolo_1.YOLO()
    if model_index == 2:
        my_yolo = yolo_2.YOLO()
    if model_index == 3:
        my_yolo = yolo_3.YOLO()
    
    Filepath = path
    print('Filepath:',Filepath)
    
    img = Filepath
    try:
        image = Image.open(img)
    except:
        print('Open Error! Try again!')
    else:
        r_image = my_yolo.detect_image(image)
        r_image=r_image.convert('RGB')
        
        
        if (r_image.size[0]>r_image.size[1]):
            print("\n\n\n")
            print("r_image size : ", r_image.size)
            print("\n\n\n")
            
            p = 416/r_image.size[1]
            out = r_image.resize((int(r_image.size[0]*p), 416))
        else:
            p = 416/r_image.size[0]
            out = r_image.resize((416, int(r_image.size[1]*p)))
        print("\n\n\n")
        print("out size : ", out.size)
        print("\n\n\n")
        out.save(path)
        
        
        #r_image.save(path)
        #r_image.show()
    keras.backend.clear_session()
    #my_yolo.close_session()