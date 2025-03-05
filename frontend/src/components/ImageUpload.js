// frontend/src/components/ImageUpload.js
import React, { useState } from "react";
import axios from "axios";
import {
  ArrowUpIcon,
  ArrowUpOnSquareIcon
} from "@heroicons/react/24/outline";

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
      <h2 className="text-xl font-bold mb-4">Identify Oral Disease</h2>
      
      {/* Row 1: Image preview and prediction result side by side */}
      <div className="flex gap-4">
        {/* Image Preview */}
        <div className="flex-1">
          {preview && (
            <img src={preview} alt="Preview" className="max-w-full h-auto border" />
          )}
        </div>
        {/* Prediction Result */}
        <div className="flex-1">
          {result && (
            result.error ? (
              <p className="text-red-500">{result.error}</p>
            ) : (
              <>
                <p>Oral Disease: {result.prediction}</p>
              </>
            )
          )}
        </div>
      </div>
      
      {/* Row 2: Upload Image and Predict buttons */}
      <div className="flex gap-4 mt-4">
        {/* Hidden file input */}
        <input 
          id="file-upload" 
          type="file" 
          onChange={handleFileChange} 
          className="hidden" 
        />
        {/* Upload Image Button */}
        <label htmlFor="file-upload" className="cursor-pointer flex items-center bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          <ArrowUpOnSquareIcon className="h-5 w-5 mr-2" />
          Upload Image
        </label>
        {/* Predict Button */}
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 flex items-center"
          onClick={handleUpload}
        >
          <ArrowUpIcon className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
};

export default ImageUpload;
