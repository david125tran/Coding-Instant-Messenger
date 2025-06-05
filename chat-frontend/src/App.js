import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [bots, setBots] = useState(["Claude", "GPT-4", "Qwen"]);
  const [selectedBot, setSelectedBot] = useState(bots[0]);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: 'you', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');

    try {
      const response = await axios.post('http://localhost:5000/chat', {
        bot: selectedBot.toLowerCase(),
        message: input,
      });
      const aiMsg = { sender: 'ai', text: response.data.reply };
      setMessages(prev => [...prev, aiMsg]);
    } catch (err) {
      console.error(err);  // Helpful for debugging
      const errorMsg = { sender: 'ai', text: 'Error getting response.' };
      setMessages(prev => [...prev, errorMsg]);
    }
  };


  return (
    <div className="App">
      <div className="sidebar">
        <h2>AI Bots</h2>
        {bots.map(bot => (
          <button
            key={bot}
            className={bot === selectedBot ? 'bot-button selected' : 'bot-button'}
            onClick={() => setSelectedBot(bot)}
          >
            {bot}
          </button>
        ))}
      </div>

      <div className="chat-section">
        <div className="chat-window">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`} style={{ width: '100%' }}>
              <div className="sender-name">{msg.sender === 'you' ? 'You' : selectedBot}</div>
              <div className="message-text">
                <ReactMarkdown
                  children={msg.text}
                  components={{
                    code({node, inline, className, children, ...props}) {
                      const match = /language-(\w+)/.exec(className || '');
                      return !inline && match ? (
                        <SyntaxHighlighter style={oneDark} language={match[1]} PreTag="div" {...props}>
                          {String(children).replace(/\n$/, '')}
                        </SyntaxHighlighter>
                      ) : (
                        <code className={className} {...props}>
                          {children}
                        </code>
                      );
                    }
                  }}
                />
              </div>
            </div>
          ))}
        </div>

        <div className="chat-form">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault(); // prevent newline
                sendMessage();
              }
            }}
            placeholder="Type a message..."
            rows={4}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
