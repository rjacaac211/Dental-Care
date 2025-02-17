import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
import tensorflow as tf

def main():
    # Set seeds for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)

    # Define the project base directory (assumes this script is in src/)
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Define paths relative to the project root
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    TRAIN_PATH = os.path.join(DATA_DIR, 'TRAIN')

    # Define image size to match MobileNetV2 expected input (224x224)
    IMG_HEIGHT, IMG_WIDTH, channels = 224, 224, 3

    # Classes: assuming 'Caries' and 'Gingivitis'
    folders = sorted(os.listdir(TRAIN_PATH))
    NUM_CATEGORIES = len(folders)
    print("Found classes:", folders)
    print("Number of categories:", NUM_CATEGORIES)

    class_to_label = {class_name: idx for idx, class_name in enumerate(folders)}
    print("Class to Label Mapping:", class_to_label)

    # Load and preprocess training images
    image_data = []
    image_labels = []

    for class_name in folders:
        class_folder = os.path.join(TRAIN_PATH, class_name)
        images = os.listdir(class_folder)
        label = class_to_label[class_name]

        for img_name in images:
            img_path = os.path.join(class_folder, img_name)
            image = Image.open(img_path).convert('RGB')
            image = image.resize((IMG_HEIGHT, IMG_WIDTH))
            image_data.append(np.array(image))
            image_labels.append(label)

    image_data = np.array(image_data)
    image_labels = np.array(image_labels)
    print("Image data shape:", image_data.shape)
    print("Image labels shape:", image_labels.shape)

    # Shuffle and split data into train and validation sets
    shuffle_indexes = np.arange(image_data.shape[0])
    np.random.shuffle(shuffle_indexes)
    image_data = image_data[shuffle_indexes]
    image_labels = image_labels[shuffle_indexes]

    X_train, X_val, y_train, y_val = train_test_split(
        image_data, image_labels, test_size=0.2, random_state=42, shuffle=True
    )

    print("X_train.shape:", X_train.shape)
    print("X_val.shape:", X_val.shape)
    print("y_train.shape:", y_train.shape)
    print("y_val.shape:", y_val.shape)

    # Save processed data as .npy files for use in train.py
    # We'll save these files in a dedicated 'processed' folder inside data/
    PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    np.save(os.path.join(PROCESSED_DIR, 'X_train.npy'), X_train)
    np.save(os.path.join(PROCESSED_DIR, 'X_val.npy'), X_val)
    np.save(os.path.join(PROCESSED_DIR, 'y_train.npy'), y_train)
    np.save(os.path.join(PROCESSED_DIR, 'y_val.npy'), y_val)

    print("Preprocessing done. Arrays saved in:", PROCESSED_DIR)

if __name__ == '__main__':
    main()
