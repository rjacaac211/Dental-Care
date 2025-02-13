import React, { useState } from "react";

const App = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [prediction, setPrediction] = useState("");

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(URL.createObjectURL(file));
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      {/* Navigation Bar */}
      <nav className="bg-gray-900 text-white py-4 px-6 flex justify-between">
        <h1 className="text-lg font-bold">RJ Dental Care PH</h1>
        <div className="space-x-4">
          <a href="#" className="hover:underline">Home</a>
          <a href="#" className="hover:underline">About</a>
          <a href="#" className="hover:underline">Products</a>
          <a href="#" className="hover:underline">Contact</a>
        </div>
      </nav>

      {/* Main Content */}
      <div className="flex flex-col items-center mt-6 px-6">
        {/* Image Upload Section */}
        <div className="flex items-center space-x-6">
          <div className="border-2 border-gray-400 p-6">
            <input
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              className="hidden"
              id="fileUpload"
            />
            <label
              htmlFor="fileUpload"
              className="cursor-pointer border border-gray-500 px-4 py-2 rounded-lg bg-gray-200 hover:bg-gray-300"
            >
              Upload Image
            </label>
            {selectedImage && (
              <img
                src={selectedImage}
                alt="Uploaded"
                className="mt-4 w-32 h-32 object-cover border"
              />
            )}
          </div>
          
          {/* Disease Prediction Display */}
          <div className="text-lg font-semibold">
            <p>Oral Disease:</p>
            <p className="text-blue-500">{prediction || "Gingivitis/Caries"}</p>
          </div>
        </div>

        {/* Chat Section */}
        <div className="w-full max-w-2xl mt-8 bg-gray-200 p-4 rounded-lg">
          <div className="h-64 bg-gray-300 rounded-lg p-4 overflow-y-auto">
            <p className="text-gray-600">Chat</p>
          </div>
          <div className="flex items-center mt-2">
            <input
              type="text"
              placeholder="Input text"
              className="flex-1 px-4 py-2 border rounded-l-lg"
            />
            <button className="bg-blue-500 text-white px-4 py-2 rounded-r-lg hover:bg-blue-600">
              ➤
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
