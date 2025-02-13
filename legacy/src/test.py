import os
import numpy as np
import pandas as pd
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from tensorflow.keras.models import load_model

# Set seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Paths
data_dir = '../data'
test_path = os.path.join(data_dir, 'TEST')
results_dir = './results'  # Directory to store all outputs
os.makedirs(results_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Assuming the same classes as in training
folders = sorted(os.listdir(test_path))
print("Test folders (Classes):", folders)
class_to_label = {class_name: idx for idx, class_name in enumerate(folders)}

# Load trained model
model = tf.keras.models.load_model('../models/oral_disease_model.h5')
print("Loaded model from ../models/oral_disease_model.h5")

# Get input shape from the model
IMG_HEIGHT, IMG_WIDTH = model.input.shape[1], model.input.shape[2]

test_data = []
test_labels = []

for class_name in folders:
    class_dir = os.path.join(test_path, class_name)
    label = class_to_label[class_name]
    images = os.listdir(class_dir)

    for img_name in images:
        img_path = os.path.join(class_dir, img_name)
        image = cv2.imread(img_path)
        if image is None:
            print("Error reading:", img_path)
            continue

        # Convert BGR to RGB and resize
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_fromarray = Image.fromarray(image, 'RGB')
        resize_image = image_fromarray.resize((IMG_WIDTH, IMG_HEIGHT))
        test_data.append(np.array(resize_image))
        test_labels.append(label)

X_test = np.array(test_data, dtype='float32') / 255.0
y_test = np.array(test_labels)

print("X_test shape:", X_test.shape)
print("y_test shape:", y_test.shape)

# Predict using the trained model
pred_probabilities = model.predict(X_test, verbose=0)
predictions = np.argmax(pred_probabilities, axis=1)

# Calculate test accuracy
test_accuracy = accuracy_score(y_test, predictions) * 100
print('Test Data Accuracy:', test_accuracy)

# Compute the confusion matrix
conf = confusion_matrix(y_test, predictions)
plt.figure(figsize=(8, 6))
sns.heatmap(conf, annot=True, fmt="d", cmap="Blues", xticklabels=folders, yticklabels=folders)
plt.xlabel('Predicted Label', fontsize=12)
plt.ylabel('True Label', fontsize=12)
plt.title('Confusion Matrix', fontsize=14)
plt.tight_layout()
confusion_matrix_path = os.path.join(results_dir, 'confusion_matrix.png')
plt.savefig(confusion_matrix_path)
print(f"Confusion matrix saved to {confusion_matrix_path}")
plt.show()

# Generate the classification report
report = classification_report(y_test, predictions, target_names=folders)
report_path = os.path.join(results_dir, 'classification_report.txt')
with open(report_path, 'w') as f:
    f.write("Classification Report:\n")
    f.write(report)
print(f"Classification report saved to {report_path}")

# Display random predictions
plt.figure(figsize=(15, 15))
random_indices = np.random.choice(len(X_test), 25, replace=False)
for i, index in enumerate(random_indices):
    plt.subplot(5, 5, i + 1)
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    prediction = predictions[index]
    actual = y_test[index]

    actual_name = folders[actual]
    prediction_name = folders[prediction]

    col = 'g' if prediction == actual else 'r'
    plt.xlabel(f'Actual: {actual_name}\nPred: {prediction_name}', color=col)
    plt.imshow(X_test[index])
plt.tight_layout()
random_predictions_path = os.path.join(results_dir, 'test_predictions_sample.png')
plt.savefig(random_predictions_path)
print(f"Sample test predictions saved to {random_predictions_path}")
plt.show()
