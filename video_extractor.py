import cv2
import os
import random
import numpy as np
import fuckit
#%%
# PARAMETERS
size_validation = 0.1 # fraction of the images used for validation set
equilibrate_classes = False # if True erases some frames in order to equilibrate the number of pictures for each class
#%%
# DIRECTORIES
dirname = os.path.dirname("__file__")
path_videos  = os.path.join(dirname, 'videos/')
path_training  = os.path.join(dirname, 'data/training_set/')
path_validation = os.path.join(dirname, 'data/validation_set/')
# generate directories
with fuckit:
    os.makedirs(path_training)
    os.makedirs(path_validation)
#%%
# INITIALIZE FUNCTIONAL VARIABLES
previous_filename = 'None'
previous_count = 0
class_counter = []
class_labels = []
#%%
# EXTRACT FRAMES FROM VIDEO TO TRAINING SET FOLDER   
for filename in os.listdir(path_videos):
    vidcap = cv2.VideoCapture(path_videos + filename)
    success, image = vidcap.read()
    count = 0
    previous_filename = previous_filename.replace('/', '')
    if previous_filename in filename:
        filename = previous_filename + '/'
        count = previous_count + 1
    with fuckit:    
        os.makedirs(path_training + filename.replace('.mp4', '/'))
    print('Processing ' + filename.replace('.mp4', '') + ' videos... ')
    while success:
        cv2.imwrite(path_training + filename.replace('.mp4', '/') + "frame%d.jpg" % count, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        count += 1
        previous_count = count
        
        if count == 1:
            class_counter.append(count)
            class_labels.append(filename.replace('.mp4', ''))
        class_counter[len(class_counter) - 1] = count
    previous_filename = filename.replace('.mp4', '')

print('--------------------------------------------------------------------')
for i in range(len(class_labels)):
    print(class_counter[i], 'elements belonging to class "', class_labels[i], '" have been generated!')   
#%%
# SHUFFLE FILES IN DIRECTORY AND SEPARATE 10% INTO VALIDATION SET
for class_index, class_count in enumerate(class_counter):
    class_array = np.arange(0, class_count)
    random.shuffle(class_array)
    count = 0
    path_class_dir = os.path.join(path_training, class_labels[class_index] + '/')
    with fuckit:
        os.makedirs(path_validation + class_labels[class_index] + '/')
    for filename in os.listdir(path_class_dir):
        with fuckit:
            if count % round(1 / size_validation) == 0:
                os.rename(os.path.join(path_class_dir, filename),
                          os.path.join(path_class_dir.replace('training_set', 'validation_set'),
                                       class_labels[class_index] + '_' + 
                                       str(class_array[count]) + '.jpg'))
            else:
                os.rename(os.path.join(path_class_dir, filename),
                          os.path.join(path_class_dir, class_labels[class_index] + '_' 
                                       + str(class_array[count]) + '.jpg'))
        count += 1
#%%
# if necessary, delete some frames in order to keep the same number for each class
min_size = int(min(class_counter) * (1 - size_validation)) 
for class_index, class_count in enumerate(class_counter):
    path_class_dir = os.path.join(path_training, class_labels[class_index] + '/')
    count = 0
    for filename in os.listdir(path_class_dir):
        count += 1
        if count >= min_size:
            os.remove(os.path.join(path_class_dir, filename))
            

