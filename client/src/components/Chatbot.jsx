import React, { useState, useRef, useEffect } from 'react';
import { BsChatDotsFill } from "react-icons/bs";
import { IoClose } from "react-icons/io5";

const qaPairs = [
  {
    question: "Where is my order?",
    answer: "You can track your order in the 'Orders' section under your profile. Deliveries typically arrive within 10-15 minutes."
  },
  {
    question: "How do I request a refund?",
    answer: "If your items are damaged or missing, please go to 'Orders', select the specific order, and tap 'Help' to request a refund."
  },
  {
    question: "Payment failed but money deducted?",
    answer: "Don't worry! If a transaction fails, the deducted amount is usually refunded within 3-5 business days. Please contact us if it takes longer than that."
  },
  {
    question: "Are there any delivery charges?",
    answer: "We offer free delivery on orders above ₹199. For orders below this amount, a small delivery fee is applied based on your location and the time of day."
  },
  {
    question: "How to contact a human agent?",
    answer: "You can call our 24/7 support line at 1-800-BLINKIT or email us at support@blinkitclone.com."
  }
];

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hi there! 👋 Welcome to Blinkit Support. How can I help you today?' }
  ]);
  const messagesEndRef = useRef(null);
  const [isTyping, setIsTyping] = useState(false);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen, isTyping]);

  const handleQuestionClick = (qa) => {
    setMessages(prev => [...prev, { sender: 'user', text: qa.question }]);
    setIsTyping(true);
    
    // Simulate thinking/typing animation delay
    setTimeout(() => {
      setIsTyping(false);
      setMessages(prev => [...prev, { sender: 'bot', text: qa.answer }]);
    }, 800);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Bot Icon Button */}
      {!isOpen && (
        <button 
          onClick={() => setIsOpen(true)}
          className="bg-green-600 hover:bg-green-700 text-white p-4 rounded-full shadow-2xl transition-all duration-300 transform hover:scale-110 flex items-center justify-center animate-bounce"
        >
          <BsChatDotsFill size={28} />
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="bg-white w-80 sm:w-96 rounded-2xl shadow-2xl border border-gray-200 flex flex-col overflow-hidden transition-all duration-300 h-[550px] max-h-[85vh]">
          {/* Header */}
          <div className="bg-green-600 text-white p-4 flex justify-between items-center shadow-sm z-10">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center text-green-600 font-bold text-xl shadow-inner">
                B
              </div>
              <div>
                <h3 className="font-bold text-md">Blinkit Assistant</h3>
                <div className="flex items-center gap-1.5">
                  <span className="w-2 h-2 bg-green-300 rounded-full animate-pulse"></span>
                  <p className="text-xs text-green-100">Online | Replies instantly</p>
                </div>
              </div>
            </div>
            <button 
              onClick={() => setIsOpen(false)}
              className="text-white hover:bg-green-700 p-1.5 rounded-full transition-colors"
            >
              <IoClose size={24} />
            </button>
          </div>

          {/* Chat Messages */}
          <div className="flex-1 p-4 overflow-y-auto bg-gray-50 flex flex-col gap-3 custom-scrollbar">
            {messages.map((msg, index) => (
              <div 
                key={index} 
                className={`max-w-[85%] p-3 rounded-2xl text-[15px] leading-relaxed ${
                  msg.sender === 'user' 
                    ? 'bg-green-600 text-white self-end rounded-tr-sm shadow-md' 
                    : 'bg-white text-gray-800 border border-gray-100 self-start rounded-tl-sm shadow-sm'
                }`}
              >
                {msg.text}
              </div>
            ))}
            
            {/* Typing Indicator */}
            {isTyping && (
              <div className="bg-white border border-gray-100 text-gray-800 self-start p-3 rounded-2xl rounded-tl-sm shadow-sm max-w-[85%]">
                <div className="flex gap-1.5 items-center h-4">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} className="h-2" />
          </div>

          {/* Preset Questions Menu */}
          <div className="p-4 bg-white border-t border-gray-100 shadow-[0_-4px_10px_rgba(0,0,0,0.02)] z-10">
             <p className="text-xs text-gray-500 font-medium mb-2.5 uppercase tracking-wide">Suggested questions</p>
            <div className="flex flex-col gap-2 overflow-y-auto max-h-40 pr-1">
              {qaPairs.map((qa, index) => (
                <button
                  key={index}
                  onClick={() => handleQuestionClick(qa)}
                  className="text-sm bg-gray-50 text-gray-700 border border-gray-200 py-2.5 px-4 rounded-xl hover:bg-green-50 hover:border-green-300 hover:text-green-700 transition-all text-left shadow-sm active:scale-[0.98]"
                >
                  {qa.question}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
