import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMsg = { text: message, sender: "user" };
    setMessages((prev) => [...prev, userMsg]);
    setMessage("");

    try {
      const response = await axios.post(
        "https://project-llm-98ms.onrender.com/api/chat",
        { message }
      );
      const aiMsg = { text: response.data.reply, sender: "ai" };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error(err);
      const errorMsg = { text: "Erreur serveur 😢", sender: "ai" };
      setMessages((prev) => [...prev, errorMsg]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      minHeight: "100vh",
      background: "linear-gradient(to right, #ffecd2, #fcb69f)",
      fontFamily: "Arial, sans-serif",
      padding: 20
    }}>
      <h1 style={{
        color: "#fff",
        textShadow: "2px 2px 4px rgba(0,0,0,0.2)"
      }}>💖 Assistant Cosmétique IA 💖</h1>

      <div style={{
        width: "100%",
        maxWidth: 500,
        height: 500,
        backgroundColor: "#fff",
        borderRadius: 25,
        padding: 20,
        boxShadow: "0 8px 16px rgba(0,0,0,0.2)",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden"
      }}>
        {/* Messages */}
        <div style={{ flex: 1, overflowY: "auto", marginBottom: 10 }}>
          {messages.map((msg, idx) => (
            <div key={idx} style={{
              display: "flex",
              justifyContent: msg.sender === "user" ? "flex-end" : "flex-start",
              marginBottom: 10
            }}>
              <div style={{
                maxWidth: "70%",
                padding: "10px 15px",
                borderRadius: 20,
                backgroundColor: msg.sender === "user" ? "#4CAF50" : "#f1f0f0",
                color: msg.sender === "user" ? "white" : "#333",
                boxShadow: "0 2px 5px rgba(0,0,0,0.1)"
              }}>
                {msg.text}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef}></div>
        </div>

        {/* Input */}
        <div style={{ display: "flex" }}>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Écris ton message..."
            style={{
              flex: 1,
              padding: 12,
              borderRadius: 25,
              border: "1px solid #ccc",
              outline: "none",
              fontSize: 16
            }}
          />
          <button
            onClick={sendMessage}
            style={{
              padding: "12px 20px",
              marginLeft: 10,
              borderRadius: 25,
              border: "none",
              backgroundColor: "#ff6b81",
              color: "white",
              fontWeight: "bold",
              cursor: "pointer",
              fontSize: 16,
              boxShadow: "0 4px 6px rgba(0,0,0,0.1)"
            }}
          >
            Envoyer
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
