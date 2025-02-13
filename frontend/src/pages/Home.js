import React from "react";
import ImageUpload from "../components/ImageUpload";
import ChatBox from "../components/ChatBox";

const Home = () => {
  return (
    <div className="container mx-auto p-4">
      <ImageUpload />
      <ChatBox />
    </div>
  );
};

export default Home;
