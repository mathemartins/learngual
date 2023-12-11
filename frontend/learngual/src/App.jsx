import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState('');
  const [socket, setSocket] = useState(null);

  // Establish WebSocket connection when component mounts
  useEffect(() => {
    const newSocket = new WebSocket('ws://127.0.0.1:8000/ws/chat/learngual/');

    newSocket.onopen = () => {
      console.log('WebSocket connected');
    };

    newSocket.onmessage = (event) => {
      const receivedMessage = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, { content: receivedMessage.message }]);

      // const receivedMessage = JSON.parse(event.data);
      // setMessages((prevMessages) => [...prevMessages, receivedMessage]);
    };

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  const sendMessage = () => {
    if (socket && messageInput.trim() !== '') {
      socket.send(JSON.stringify({ message: messageInput.trim() }));
      setMessageInput('');
    }
  };

  const handleInputChange = (e) => {
    setMessageInput(e.target.value);
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className="message">
            <p>{msg.content}</p>
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          placeholder="Type your message..."
          value={messageInput}
          onChange={handleInputChange}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App
