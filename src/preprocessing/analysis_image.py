import os
from PIL import Image
import tensorflow as tf
import matplotlib.pyplot as plt

# Resize and normalize images
def resize_and_normalize_images(input_folder, output_folder, size=(128, 128)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for subdir, _, files in os.walk(input_folder):
        for file in files:
            filepath = os.path.join(subdir, file)
            image = Image.open(filepath).convert('RGB')
            image = image.resize(size)
            output_path = os.path.join(output_folder, os.path.relpath(filepath, input_folder))
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # Ensure the file extension is valid
            if output_path.lower().endswith(('.jpeg', '.jpg', '.png')):
                image.save(output_path)
            else:
                image.save(output_path + '.png')

resize_and_normalize_images('dataset/train', 'dataset_resized/train')
resize_and_normalize_images('dataset/validation', 'dataset_resized/validation')
resize_and_normalize_images('dataset/test', 'dataset_resized/test')

# Normalize images
def normalize_image(image):
    image = tf.image.convert_image_dtype(image, tf.float32)
    return image

# Create datasets
def create_dataset(directory, batch_size=32, shuffle=True):
    dataset = tf.keras.preprocessing.image_dataset_from_directory(
        directory,
        image_size=(128, 128),
        batch_size=batch_size,
        label_mode='int'
    )
    if shuffle:
        dataset = dataset.shuffle(buffer_size=1000)
    dataset = dataset.map(lambda x, y: (normalize_image(x), y))
    return dataset

# Data augmentation
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal_and_vertical"),
    tf.keras.layers.RandomRotation(0.2),
    tf.keras.layers.RandomZoom(0.2),
])

def augment_dataset(dataset):
    return dataset.map(lambda x, y: (data_augmentation(x, training=True), y))

# Create and augment train dataset
train_dataset = create_dataset('dataset_resized/train', batch_size=32, shuffle=True)
train_dataset = augment_dataset(train_dataset)

# Create validation and test datasets
validation_dataset = create_dataset('dataset_resized/validation', batch_size=32, shuffle=False)
test_dataset = create_dataset('dataset_resized/test', batch_size=32, shuffle=False)

# Example to visualize a batch of images
def visualize_dataset(dataset, class_names, batch_size=32):
    plt.figure(figsize=(15, 15))
    for images, labels in dataset.take(1):
        for i in range(batch_size):
            ax = plt.subplot(4, 8, i + 1)
            plt.imshow(images[i].numpy())
            plt.title(class_names[labels[i]])
            plt.axis("off")
    plt.show()

class_names = ['white_ball', 'orange_ball', 'obstacle', 'wall', 'egg']
visualize_dataset(train_dataset, class_names)
