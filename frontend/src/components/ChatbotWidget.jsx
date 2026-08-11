import React, { useState, useRef, useEffect } from "react";
import { MessageCircle, X, Send, Bot } from "lucide-react";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function ChatbotWidget() {
  const { user } = useAuth();
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: "bot", text: "Hi! I'm your AI travel assistant. Ask me about budgets, weather, packing, safety, or itineraries!" },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, open]);

  if (!user) return null;

  const sendMessage = async () => {
    const text = input.trim();
    if (!text || sending) return;

    setMessages((m) => [...m, { role: "user", text }]);
    setInput("");
    setSending(true);

    try {
      const res = await api.post("/chatbot/ask", { message: text });
      setMessages((m) => [...m, { role: "bot", text: res.data.response }]);
    } catch {
      setMessages((m) => [...m, { role: "bot", text: "Sorry, I'm having trouble responding right now." }]);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {open && (
        <div className="w-80 h-96 bg-white rounded-xl2 shadow-card-hover flex flex-col mb-3 overflow-hidden border border-gray-100">
          <div className="bg-primary-500 text-white px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-2 font-semibold text-sm">
              <Bot size={18} /> Travel Assistant
            </div>
            <button onClick={() => setOpen(false)}><X size={18} /></button>
          </div>
          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            {messages.map((m, i) => (
              <div key={i} className={`text-sm max-w-[85%] px-3 py-2 rounded-xl ${m.role === "user" ? "ml-auto bg-primary-500 text-white" : "bg-gray-100 text-ink-700"}`}>
                {m.text}
              </div>
            ))}
            <div ref={bottomRef} />
          </div>
          <div className="p-2 border-t border-gray-100 flex gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              placeholder="Ask me anything..."
              className="input-field text-sm"
            />
            <button onClick={sendMessage} className="bg-primary-500 text-white p-2.5 rounded-xl">
              <Send size={16} />
            </button>
          </div>
        </div>
      )}
      <button
        onClick={() => setOpen(!open)}
        className="bg-primary-500 hover:bg-primary-600 text-white p-4 rounded-full shadow-card-hover"
      >
        {open ? <X size={22} /> : <MessageCircle size={22} />}
      </button>
    </div>
  );
}
