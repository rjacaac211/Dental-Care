import numpy as np
import cv2
from tensorflow.keras.models import load_model
import os

class CVAgent:
    def __init__(self, model_path: str):
        self.model = load_model(model_path)
        self.class_labels = ["Caries", "Gingivitis"]

    def preprocess_image(self, image_path: str):
        # Read the image using OpenCV (returns BGR format)
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image at path '{image_path}' could not be read")
        # Convert from BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Resize the image to 224x224
        img = cv2.resize(img, (224, 224))
        # Normalize the pixel values to [0, 1]
        img_array = img.astype("float32") / 255.0
        # Expand dimensions to create a batch of size 1
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    def predict(self, image_path: str):
        img_array = self.preprocess_image(image_path)
        predictions = self.model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]
        confidence = np.max(predictions) * 100
        return self.class_labels[predicted_class], round(confidence, 2)
