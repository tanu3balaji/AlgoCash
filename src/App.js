import { useState } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [typingSpeed, setTypingSpeed] = useState(0);
  const [securityQuestion, setSecurityQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  let keyPressTime = 0;
  let lastKeyReleaseTime = 0;

  const handleKeyDown = () => {
    keyPressTime = performance.now();
  };

  const handleKeyUp = (event) => {
    const keyReleaseTime = performance.now();
    const newTypingSpeed = event.target.value.length / (keyReleaseTime / 1000);
    setTypingSpeed(newTypingSpeed);
    sendTypingData(newTypingSpeed);
  };

  const sendTypingData = async (speed) => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/keystroke-data", {
        user_id: "user123",
        typing_speed: speed,
      });

      if (response.data.action === "Trigger Security Question") {
        setSecurityQuestion(response.data.question);
      } else {
        alert("Login successful!");
      }
    } catch (error) {
      console.error("Error sending typing data:", error);
    }
  };

  const handleSecurityAnswer = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/verify-security-answer", {
        user_id: "user123",
        answer,
      });

      if (response.data.status === "Authenticated") {
        alert("Access Granted!");
      } else {
        alert("Incorrect Answer. Access Denied.");
      }
    } catch (error) {
      console.error("Error verifying security answer:", error);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input type="text" onKeyDown={handleKeyDown} onKeyUp={handleKeyUp} placeholder="Type your username" />

      {securityQuestion && (
        <div>
          <p>{securityQuestion}</p>
          <input type="text" value={answer} onChange={(e) => setAnswer(e.target.value)} placeholder="Enter answer" />
          <button onClick={handleSecurityAnswer}>Submit Answer</button>
        </div>
      )}
    </div>
  );
};

export default App;