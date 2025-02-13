import React, { useState } from "react";

const ChatBox = () => {
  const [chatInput, setChatInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSend = () => {
    if (!chatInput.trim()) return;

    const userMessage = chatInput.trim();
    let botResponse = "";
    const lowerInput = userMessage.toLowerCase();

    if (lowerInput === "book appointment") {
      botResponse = "Appointment booked successfully.";
    } else if (lowerInput === "get appointments") {
      botResponse = "Appointments: [ { id: 1, date: '2025-03-01', time: '10:00 AM' } ]";
    } else if (lowerInput === "web search") {
      botResponse = "Search results for 'web search' will appear here.";
    } else {
      botResponse = "I'm sorry, I didn't understand that command.";
    }

    setMessages([
      ...messages,
      { sender: "You", text: userMessage },
      { sender: "Bot", text: botResponse },
    ]);
    setChatInput("");
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
        />
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded-r-lg hover:bg-blue-600"
          onClick={handleSend}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatBox;
