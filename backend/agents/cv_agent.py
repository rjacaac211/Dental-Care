# backend/agents/cv_agent.py
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import os

class CVAgent:
    def __init__(self, model_path: str):
        self.model = load_model(model_path)
        self.class_labels = ["Caries", "Gingivitis"]

    def preprocess_image(self, image_path: str):
        img = Image.open(image_path).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    
    def predict(self, image_path: str):
        img_array = self.preprocess_image(image_path)
        predictions = self.model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]
        confidence = np.max(predictions) * 100
        return self.class_labels[predicted_class], round(confidence, 2)
    
if __name__ == "__main__":
    model_path = os.path.join(os.path.dirname(__file__), "../models/oral_disease_model.h5")
    agent = CVAgent(model_path)
    prediction, confidence = agent.predict("path_to_sample_image.jpg")
    print(f"Prediction: {prediction}, Confidence: {confidence}%")