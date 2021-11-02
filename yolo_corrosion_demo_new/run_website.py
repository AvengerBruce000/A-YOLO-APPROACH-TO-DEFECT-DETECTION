import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from yolo_video import main
import shutil  
import time


ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def find_old_file(directory):
    file_lists = os.listdir(directory)
    file_lists.sort(key=lambda fn: os.path.getmtime(directory + "/" + fn)
                    if not os.path.isdir(directory + "/" + fn) else 0)
    file = os.path.join(directory, file_lists[0])
    return file



def file_counter(directory):
    count = 0
    for root,dirs,files in os.walk(directory):   
        for each in files:
            count += 1   
    return count


	
@app.route('/')
def upload_form():
	return render_template('upload.html')







@app.route('/upload_image_testing', methods=['POST'])
def upload_image_testing():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        
        ######################################################
        # clean the folder
        #shutil.rmtree(app.config['UPLOAD_FOLDER'])  
        #os.mkdir(app.config['UPLOAD_FOLDER'])  
        #when the number of images in the buffer exceeds a certain value, clean the old images
        while file_counter(app.config['UPLOAD_FOLDER']) > 20:
            os.remove(find_old_file(app.config['UPLOAD_FOLDER']))
        ######################################################
        filename =  'model_testing_' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + '.jpg'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        ##########################
        main(os.path.join(app.config['UPLOAD_FOLDER'], filename), 0)
        ##########################
		#print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> jpg, jpeg')
        return redirect(request.url)

@app.route('/upload_image_1', methods=['POST'])
def upload_image_1():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        
        ######################################################
        # clean the folder
        #shutil.rmtree(app.config['UPLOAD_FOLDER'])  
        #os.mkdir(app.config['UPLOAD_FOLDER'])  
        #when the number of images in the buffer exceeds a certain value, clean the old images
        while file_counter(app.config['UPLOAD_FOLDER']) > 20:
            os.remove(find_old_file(app.config['UPLOAD_FOLDER']))
        ######################################################
        filename = 'model_1_' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + '.jpg'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        ##########################
        main(os.path.join(app.config['UPLOAD_FOLDER'], filename), 1)
        ##########################
		#print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> jpg, jpeg')
        return redirect(request.url)

@app.route('/upload_image_2', methods=['POST'])
def upload_image_2():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        
        ######################################################
        # clean the folder
        #shutil.rmtree(app.config['UPLOAD_FOLDER'])  
        #os.mkdir(app.config['UPLOAD_FOLDER'])  
        #when the number of images in the buffer exceeds a certain value, clean the old images
        while file_counter(app.config['UPLOAD_FOLDER']) > 20:
            os.remove(find_old_file(app.config['UPLOAD_FOLDER']))
        ######################################################
        filename =  'model_2_' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + '.jpg'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        ##########################
        main(os.path.join(app.config['UPLOAD_FOLDER'], filename), 2)
        ##########################
		#print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> jpg, jpeg')
        return redirect(request.url)

@app.route('/upload_image_3', methods=['POST'])
def upload_image_3():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        
        ######################################################
        # clean the folder
        #shutil.rmtree(app.config['UPLOAD_FOLDER'])  
        #os.mkdir(app.config['UPLOAD_FOLDER'])  
        #when the number of images in the buffer exceeds a certain value, clean the old images
        while file_counter(app.config['UPLOAD_FOLDER']) > 20:
            os.remove(find_old_file(app.config['UPLOAD_FOLDER']))
        ######################################################
        filename =  'model_3_' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + '.jpg'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        ##########################
        main(os.path.join(app.config['UPLOAD_FOLDER'], filename), 3)
        ##########################
		#print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> jpg, jpeg')
        return redirect(request.url)





















@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3389)
    #app.run()