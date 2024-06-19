import os
import shutil
from sklearn.model_selection import train_test_split

# create a directory to store the extracted images
extracted_dir = 'extracted_images'

# create dataset directory
dataset_dir = 'dataset'
train_dir = os.path.join(dataset_dir, 'train')
val_dir = os.path.join(dataset_dir, 'validation')
test_dir = os.path.join(dataset_dir, 'test')

# create directories for each label
labels = ['white_ball', 'orange_ball']
for label in labels:
    os.makedirs(os.path.join(train_dir, label), exist_ok=True)
    os.makedirs(os.path.join(val_dir, label), exist_ok=True)
    os.makedirs(os.path.join(test_dir, label), exist_ok=True)

# split the extracted images into train, validation, and test sets
for label in labels:
    images = [f for f in os.listdir(extracted_dir) if label in f]
    train_and_val, test = train_test_split(images, test_size=0.2)
    train, val = train_test_split(train_and_val, test_size=0.1)

   # copy images to the appropriate directories
    for image in train:
        shutil.copy(os.path.join(extracted_dir, image), os.path.join(train_dir, label))
    for image in val:
        shutil.copy(os.path.join(extracted_dir, image), os.path.join(val_dir, label))
    for image in test:
        shutil.copy(os.path.join(extracted_dir, image), os.path.join(test_dir, label))

print("Sorted the images into dataset")
