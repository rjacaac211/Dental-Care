import React, { useState, useEffect } from "react";
import axios from "axios";

const ChatBox = () => {
  const [chatInput, setChatInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // On mount, generate or retrieve session ID
    let storedSession = localStorage.getItem("dental_session_id");
    if (!storedSession) {
      storedSession = `sess-${Date.now()}`;
      localStorage.setItem("dental_session_id", storedSession);
    }
    setSessionId(storedSession);
  }, []);

  const handleSend = async () => {
    if (!chatInput.trim()) return;

    const userMessage = chatInput.trim();
    setMessages((prev) => [...prev, { sender: "You", text: userMessage }]);
    setChatInput("");
    setIsLoading(true);

    try {
      // NOTE: We now send session_id
      const response = await axios.post("http://localhost:8000/api/chat", {
        session_id: sessionId,
        message: userMessage,
      });
      const botResponse = response.data.final_response || "No response";
      setMessages((prev) => [...prev, { sender: "Bot", text: botResponse }]);
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prev) => [...prev, { sender: "Bot", text: "Error processing your request." }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
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
          messages.map((msg, idx) => (
            <div key={idx} className="mb-2">
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
