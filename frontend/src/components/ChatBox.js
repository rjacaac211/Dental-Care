import React, { useState } from "react";
import axios from "axios"; // Make sure you have axios installed

const ChatBox = () => {
  const [chatInput, setChatInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!chatInput.trim()) return;

    const userMessage = chatInput.trim();
    // Add the user's message to the conversation
    setMessages([...messages, { sender: "You", text: userMessage }]);
    setChatInput("");
    setIsLoading(true);

    try {
      // Make a request to your FastAPI endpoint
      const response = await axios.post("http://localhost:8000/api/chat", {
        message: userMessage,
      });

      const botResponse = response.data.final_response || response.data.final_response || "No response";
      // Update the conversation with the bot's response
      setMessages((prev) => [
        ...prev,
        { sender: "Bot", text: botResponse },
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "Bot", text: "Error processing your request." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    // Send the message if user presses Enter
    if (e.key === "Enter") {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="bg-gray-200 p-4 rounded-lg mt-8 max-w-2xl mx-auto">
      <div className="bg-gray-300 rounded-lg p-4 h-64 overflow-y-auto">
        {messages.length === 0 ? (
          <p className="text-gray-600">Chat conversation will appear here...</p>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className="mb-2">
              <strong>{msg.sender}:</strong> {msg.text}
            </div>
          ))
        )}
      </div>
      <div className="flex mt-2">
        <input
          type="text"
          className="flex-1 px-4 py-2 border rounded-l-lg"
          placeholder="Type your message..."
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
        />
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded-r-lg hover:bg-blue-600"
          onClick={handleSend}
          disabled={isLoading}
        >
          {isLoading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default ChatBox;
