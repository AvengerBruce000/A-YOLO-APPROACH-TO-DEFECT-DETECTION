import argparse
from yolo import YOLO
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw() 
def detect_img(yolo):
    while True:
             

        Filepath = filedialog.askopenfilename()
        print('Filepath:',Filepath)
        if(Filepath==''):
            break
        
        img = Filepath
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            r_image = yolo.detect_image(image)
            ################################################
            (filepath, tempfilename) = os.path.split(img)
            (filename, extension) = os.path.splitext(tempfilename)
            r_image.save("./results/" + filename + ".png")
            ################################################
            r_image.show()
    yolo.close_session()

FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    FLAGS = parser.parse_args()
    """
    Image detection mode, disregard any remaining command line arguments
    """
    print("Image detection mode")
    if "input" in FLAGS:
        print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
    detect_img(YOLO(**vars(FLAGS)))

