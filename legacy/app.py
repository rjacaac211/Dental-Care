import os
import shutil
import numpy as np
from flask import Flask, request, render_template, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import atexit  # For cleanup on app exit

# Initialize Flask app
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the trained model
model_path = "models/oral_disease_model.h5"
model = load_model(model_path)

# Define class labels
class_labels = ["Caries", "Gingivitis"]

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Home Route - Upload Form
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if file is uploaded
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        # Save the uploaded file
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Predict the uploaded image
        prediction, confidence = predict_image(filename)

        return render_template('result.html', prediction=prediction, confidence=confidence, image_path=filename)

    return render_template('index.html')

# Prediction Function
def predict_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))  # Resize to match the model input
    img_array = np.array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Predict
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    confidence = np.max(predictions) * 100  # Confidence in percentage

    return class_labels[predicted_class], round(confidence, 2)

# Cleanup Function to Delete All Uploaded Files
def cleanup_uploaded_files():
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)  # Delete the entire upload folder
        print(f"All uploaded files in '{UPLOAD_FOLDER}' have been deleted.")

# Register cleanup function to run when the app stops
atexit.register(cleanup_uploaded_files)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
