// frontend/src/components/ImageUpload.js
import React, { useState } from "react";
import axios from "axios";

const ImageUpload = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await axios.post("http://localhost:8000/api/predict", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      console.log("Response from API:", response.data);
      setResult(response.data);
    } catch (error) {
      console.error("Error during image prediction:", error);
      setResult({ error: "Error in prediction" });
    }
  };

  return (
    <div className="max-w-md mx-auto border p-4 rounded-lg">
      <h2 className="text-xl font-bold mb-4">Image Prediction</h2>
      <input type="file" onChange={handleFileChange} />
      {preview && (
        <div className="mt-4">
          <img src={preview} alt="Preview" className="w-32 h-32 object-cover border" />
        </div>
      )}
      <button
        className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        onClick={handleUpload}
      >
        Upload & Predict
      </button>
      {result && (
        <div className="mt-4">
          {result.error ? (
            <p className="text-red-500">{result.error}</p>
          ) : (
            <>
              <p>Prediction: {result.prediction}</p>
              <p>Confidence: {result.confidence}%</p>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
