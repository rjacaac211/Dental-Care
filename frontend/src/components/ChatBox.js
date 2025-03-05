import React, { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import axios from "axios";
import {
  PaperAirplaneIcon,
  ArrowPathIcon,
  MicrophoneIcon,
  StopIcon
} from "@heroicons/react/24/outline";

const ChatBox = () => {
  const [chatInput, setChatInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // --- STATES FOR SPEECH TO TEXT ---
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // --- CHAT HISTORY LOGIC ---
  // On mount, generate or retrieve session ID and load chat history
  useEffect(() => {
    let storedSession = localStorage.getItem("dental_session_id");
    if (!storedSession) {
      storedSession = `sess-${Date.now()}`;
      localStorage.setItem("dental_session_id", storedSession);
    }
    setSessionId(storedSession);
  }, []);

  // Fetch chat history when sessionId is available
  useEffect(() => {
    if (!sessionId) return;
    // Once sessionId is available, load chat history
    const fetchChatHistory = async () => {
      try {
        const res = await axios.get(`http://localhost:8000/api/chat_history/${sessionId}`);
        if (res.data.chat_history) {
          // // Sort by timestamp if needed
          // const sortedMessages = res.data.chat_history.sort((a, b) => a.timestamp - b.timestamp);
          // Map history documents to local message format
          const loadedMessages = res.data.chat_history.map((msg) => ({
            sender: msg.sender,
            text: msg.message,
          }));
          setMessages(loadedMessages);
        }
      } catch (error) {
        console.error("Error fetching chat history:", error);
      }
    };

    fetchChatHistory();
  }, [sessionId]);

  // Helper function: Save chat message to backend
  const saveChatMessage = async (sender, message) => {
    try {
      console.log("Saving chat message:", {
        session_id: sessionId,
        sender,
        message,
      });
      await axios.post("http://localhost:8000/api/save_chat", {
        session_id: sessionId,
        sender,
        message,
      });
      console.log("Chat message saved successfully.");
    } catch (error) {
      console.error("Error saving chat message:", error);
    }
  };


  // ------------- SEND TEXT MESSAGE -------------
  const handleSend = async () => {
    if (!chatInput.trim()) return;
    const userMessage = chatInput.trim();

    // Update local UI immediately
    setMessages((prev) => [...prev, { sender: "You", text: userMessage }]);
    setChatInput("");
    setIsLoading(true);

    // Save user message to DB
    await saveChatMessage("You", userMessage);

    try {
      // Send the message to the chat API
      const response = await axios.post("http://localhost:8000/api/chat", {
        session_id: sessionId,
        message: userMessage,
      });
      const botResponse = response.data.final_response || "No response";
      setMessages((prev) => [...prev, { sender: "Bot", text: botResponse }]);

      // Save bot response to DB
      await saveChatMessage("Bot", botResponse);
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prev) => [...prev, { sender: "Bot", text: "Error processing your request." },
        ...prev,
        { sender: "Bot", text: "Error processing your request." }
      ]);
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

  // ------------- SPEECH TO TEXT LOGIC -------------

  const handleRecordToggle = async () => {
    if (!isRecording) {
      // Start recording
      setIsRecording(true);
      audioChunksRef.current = []; // reset the chunks

      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;

        // On dataavailable is called every time we get a chunk of audio
        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data);
          }
        };

        // On stop is triggered after we call mediaRecorder.stop()
        mediaRecorder.onstop = async () => {
          // Combine all chunks into one Blob
          const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
          // Optionally: send to backend
          await sendAudioForTranscription(audioBlob);
        };

        mediaRecorder.start();
      } catch (err) {
        console.error("Could not start recording:", err);
        setIsRecording(false);
      }
    } else {
      // Stop recording
      setIsRecording(false);
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop();
      }
    }
  };

  const sendAudioForTranscription = async (audioBlob) => {
    try {
      setIsLoading(true);

      // Create form data
      const formData = new FormData();
      formData.append("file", audioBlob, "recording.wav");
      formData.append("session_id", sessionId);

      // POST to your STT endpoint (e.g. /api/transcribe)
      const res = await axios.post("http://localhost:8000/api/transcribe", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const transcript = res.data.transcript || "";
      // Option 1: Insert the transcript into chatInput
      setChatInput(transcript);

      // Option 2 (Automatic send):
      // setMessages((prev) => [...prev, { sender: "You", text: transcript }]);
      // handleSend(transcript);

    } catch (error) {
      console.error("Error transcribing audio:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // ------------- RENDER -------------
  return (
    <div className="bg-gray-200 p-6 rounded-lg mt-8 max-w-4xl mx-auto">
      <div className="bg-gray-300 rounded-lg p-4 h-96 overflow-y-auto space-y-2">
        {messages.length === 0 ? (
          <p className="text-gray-600">Chat conversation will appear here...</p>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.sender === "You" ? "justify-end" : "justify-start"}`}>
              <div className={`rounded-lg p-3 max-w-md break-words ${msg.sender === "You" ? "bg-blue-500 text-white" : "bg-gray-100 text-gray-800"}`}>
                <div className="markdown-content">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {msg.text}
                  </ReactMarkdown>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
      <div className="flex mt-4">
      <button
          onClick={handleRecordToggle}
          className={`${
            isRecording ? "bg-gray-500" : "bg-blue-500"
          } text-white px-4 py-2 hover:opacity-90`}
        >
            {isRecording ? (
              <StopIcon className="w-5 h-5" />
            ) : (
              <MicrophoneIcon className="w-5 h-5" />
            )}
          {/* {isRecording ? "Stop Recording" : "Start Recording"} */}
        </button>
        <input
          type="text"
          className="flex-1 px-4 py-2 border"
          placeholder="Type your message..."
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
        />
        <button
          className="bg-blue-500 text-white px-4 py-2 hover:bg-blue-600"
          onClick={handleSend}
          disabled={isLoading}
        >
          {isLoading ? (
            <ArrowPathIcon className="w-5 h-5 animate-spin" />
          ) : (
            <PaperAirplaneIcon className="w-5 h-5 transform" />
          )}
          {/* {isLoading ? "Sending..." : "Send"} */}
        </button>
      </div>   
    </div>
  );
};

export default ChatBox;
